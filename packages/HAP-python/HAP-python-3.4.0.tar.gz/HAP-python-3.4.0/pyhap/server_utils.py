from pyhap import tlv
from pyhap.util import long_to_bytes

from Crypto.Hash import SHA512
from Crypto.Protocol.KDF import HKDF
from tlslite.utils.chacha20_poly1305 import CHACHA20_POLY1305
import curve25519
import ed25519

import json
import logging
import uuid

__all__ = (
    'BaseHapRequestHandler',
    'pad_tls_nonce',
    'hap_hkdf',
    'HAP_TLV_TAGS'
)


# Various "tag" constants for HAP's TLV encoding.
class HAP_TLV_TAGS:
    REQUEST_TYPE = b'\x00'
    USERNAME = b'\x01'
    SALT = b'\x02'
    PUBLIC_KEY = b'\x03'
    PASSWORD_PROOF = b'\x04'
    ENCRYPTED_DATA = b'\x05'
    SEQUENCE_NUM = b'\x06'
    ERROR_CODE = b'\x07'
    PROOF = b'\x0A'


# Status codes for underlying HAP calls
class HAP_SERVER_STATUS:
    SUCCESS = 0
    INSUFFICIENT_PRIVILEGES = -70401
    SERVICE_COMMUNICATION_FAILURE = -70402
    RESOURCE_BUSY = -70403
    READ_ONLY_CHARACTERISTIC = -70404
    WRITE_ONLY_CHARACTERISTIC = -70405
    NOTIFICATION_NOT_SUPPORTED = -70406
    OUT_OF_RESOURCE = -70407
    OPERATION_TIMED_OUT = -70408
    RESOURCE_DOES_NOT_EXIST = -70409
    INVALID_VALUE_IN_REQUEST = -70410


# Error codes and the like, guessed by packet inspection
class HAP_OPERATION_CODE:
    INVALID_REQUEST = b'\x02'
    INVALID_SIGNATURE = b'\x04'


class HAP_CRYPTO:
    HKDF_KEYLEN = 32  # bytes, length of expanded HKDF keys
    HKDF_HASH = SHA512  # Hash function to use in key expansion
    TLS_NONCE_LEN = 12  # bytes, length of TLS encryption nonce


def pad_tls_nonce(nonce, total_len=HAP_CRYPTO.TLS_NONCE_LEN):
    """Pads a nonce with zeroes so that total_len is reached."""
    return nonce.rjust(total_len, b"\x00")


def hap_hkdf(key, salt, info):
    """Just a shorthand."""
    return HKDF(key, HAP_CRYPTO.HKDF_KEYLEN, salt, HAP_CRYPTO.HKDF_HASH, context=info)


class UnprivilegedRequestException(Exception):
    pass


class NotAllowedInStateException(Exception):
    pass


PAIRING_3_SALT = b"Pair-Setup-Encrypt-Salt"
PAIRING_3_INFO = b"Pair-Setup-Encrypt-Info"
PAIRING_3_NONCE = pad_tls_nonce(b"PS-Msg05")

PAIRING_4_SALT = b"Pair-Setup-Controller-Sign-Salt"
PAIRING_4_INFO = b"Pair-Setup-Controller-Sign-Info"

PAIRING_5_SALT = b"Pair-Setup-Accessory-Sign-Salt"
PAIRING_5_INFO = b"Pair-Setup-Accessory-Sign-Info"
PAIRING_5_NONCE = pad_tls_nonce(b"PS-Msg06")

PVERIFY_1_SALT = b"Pair-Verify-Encrypt-Salt"
PVERIFY_1_INFO = b"Pair-Verify-Encrypt-Info"
PVERIFY_1_NONCE = pad_tls_nonce(b"PV-Msg02")

PVERIFY_2_NONCE = pad_tls_nonce(b"PV-Msg03")


class BaseHapRequestHandler:

    __slots__ = ('_accessory_driver', '_state')

    def __init__(self, accessory_driver):
        self._accessory_driver = accessory_driver
        self._state = accessory_driver.state

    def _handle_pairing(self, indata):

        tlv_objects = tlv.decode(indata)
        sequence = tlv_objects[HAP_TLV_TAGS.SEQUENCE_NUM]

        if sequence == b'\x01':
            return self._pairing_one()
        elif sequence == b'\x03':
            return self._pairing_two(tlv_objects)
        elif sequence == b'\x05':
            return self._pairing_three(tlv_objects)
        else:
            raise ValueError('Unkown pairing sequence number')

    def _pairing_one(self):
        """Send the SRP salt and public key to the client.

        The SRP verifier is created at this step.
        """
        logging.debug("Pairing [1/5]")
        self._accessory_driver.setup_srp_verifier()
        salt, B = self._accessory_driver.srp_verifier.get_challenge()

        return tlv.encode(HAP_TLV_TAGS.SEQUENCE_NUM, b'\x02',
                          HAP_TLV_TAGS.SALT, salt,
                          HAP_TLV_TAGS.PUBLIC_KEY, long_to_bytes(B))

    def _pairing_two(self, tlv_objects):
        """Obtain the challenge from the client (A) and client's proof that it
        knows the password (M). Verify M and generate the server's proof based on
        A (H_AMK). Send the H_AMK to the client.

        @param tlv_objects: The TLV data received from the client.
        @type tlv_object: dict
        """
        logging.debug("Pairing [2/5]")
        A = tlv_objects[HAP_TLV_TAGS.PUBLIC_KEY]
        M = tlv_objects[HAP_TLV_TAGS.PASSWORD_PROOF]
        verifier = self._accessory_driver.srp_verifier
        verifier.set_A(A)

        hamk = verifier.verify(M)

        if hamk is None:  # Probably the provided pincode was wrong.
            return tlv.encode(HAP_TLV_TAGS.SEQUENCE_NUM, b'\x04',
                              HAP_TLV_TAGS.ERROR_CODE,
                              HAP_OPERATION_CODE.INVALID_REQUEST)

        return tlv.encode(HAP_TLV_TAGS.SEQUENCE_NUM, b'\x04',
                          HAP_TLV_TAGS.PASSWORD_PROOF, hamk)

    def _pairing_three(self, tlv_objects):
        """Expand the SRP session key to obtain a new key. Use it to verify and decrypt
            the recieved data. Continue to step four.

        @param tlv_objects: The TLV data received from the client.
        @type tlv_object: dict
        """
        logging.debug("Pairing [3/5]")
        encrypted_data = tlv_objects[HAP_TLV_TAGS.ENCRYPTED_DATA]

        session_key = self._accessory_driver.srp_verifier.get_session_key()
        hkdf_enc_key = hap_hkdf(long_to_bytes(session_key),
                                PAIRING_3_SALT, PAIRING_3_INFO)

        cipher = CHACHA20_POLY1305(hkdf_enc_key, "python")
        decrypted_data = cipher.open(PAIRING_3_NONCE, bytearray(encrypted_data), b"")
        assert decrypted_data is not None

        dec_tlv_objects = tlv.decode(bytes(decrypted_data))
        client_username = dec_tlv_objects[HAP_TLV_TAGS.USERNAME]
        client_ltpk = dec_tlv_objects[HAP_TLV_TAGS.PUBLIC_KEY]
        client_proof = dec_tlv_objects[HAP_TLV_TAGS.PROOF]

        return self._pairing_four(client_username, client_ltpk, client_proof, hkdf_enc_key)

    def _pairing_four(self, client_username, client_ltpk, client_proof, encryption_key):
        """Expand the SRP session key to obtain a new key.
            Use it to verify that the client's proof of the private key. Continue to
            step five.

        @param client_username: The client's username.
        @type client_username: bytes.

        @param client_ltpk: The client's public key.
        @type client_ltpk: bytes

        @param client_proof: The client's proof of password.
        @type client_proof: bytes

        @param encryption_key: The encryption key for this step.
        @type encryption_key: bytes
        """
        logging.debug("Pairing [4/5]")
        session_key = self._accessory_driver.srp_verifier.get_session_key()
        output_key = hap_hkdf(long_to_bytes(session_key),
                              PAIRING_4_SALT, PAIRING_4_INFO)

        data = output_key + client_username + client_ltpk
        verifying_key = ed25519.VerifyingKey(client_ltpk)

        try:
            verifying_key.verify(client_proof, data)
        except ed25519.BadSignatureError:
            logging.error("Bad signature, abort.")
            raise

        return self._pairing_five(client_username, client_ltpk, encryption_key)

    def _pairing_five(self, client_username, client_ltpk, encryption_key):
        """At that point we know the client has the accessory password and has a valid key
        pair. Add it as a pair and send a sever proof.

        Parameters are as for _pairing_four.
        """
        logging.debug("Pairing [5/5]")
        session_key = self._accessory_driver.srp_verifier.get_session_key()
        output_key = hap_hkdf(long_to_bytes(session_key),
                              PAIRING_5_SALT, PAIRING_5_INFO)

        server_public = self._state.public_key.to_bytes()
        mac = self._state.mac.encode()

        material = output_key + mac + server_public
        private_key = self._state.private_key
        server_proof = private_key.sign(material)

        message = tlv.encode(HAP_TLV_TAGS.USERNAME, mac,
                             HAP_TLV_TAGS.PUBLIC_KEY, server_public,
                             HAP_TLV_TAGS.PROOF, server_proof)

        cipher = CHACHA20_POLY1305(encryption_key, "python")
        aead_message = bytes(
            cipher.seal(PAIRING_5_NONCE, bytearray(message), b""))

        client_uuid = uuid.UUID(str(client_username, "utf-8"))
        should_confirm = self._accessory_driver.pair(client_uuid, client_ltpk)

        if not should_confirm:
            self.send_response(500)
            return

        return tlv.encode(HAP_TLV_TAGS.SEQUENCE_NUM, b'\x06',
                          HAP_TLV_TAGS.ENCRYPTED_DATA, aead_message)

    def _handle_pair_verify(self, indata, enc_context=None):
        """Handles arbitrary step of the pair verify process.

        Pair verify is session negotiation.
        """
        if not self._state.paired:
            raise NotAllowedInStateException

        tlv_objects = tlv.decode(indata)
        sequence = tlv_objects[HAP_TLV_TAGS.SEQUENCE_NUM]
        if sequence == b'\x01':
            return self._pair_verify_one(tlv_objects)
        elif sequence == b'\x03':
            if enc_context is None:
                raise ValueError('Encyrption context must be given when executing '
                                 'the second pair verify step')
            return self._pair_verify_two(tlv_objects, enc_context)
        else:
            raise ValueError('Unknown pair verify sequence number')

    def _pair_verify_one(self, tlv_objects):
        """Generate new session key pair and send a proof to the client.

        @param tlv_objects: The TLV data received from the client.
        @type tlv_object: dict
        """
        logging.debug("Pair verify [1/2].")
        client_public = tlv_objects[HAP_TLV_TAGS.PUBLIC_KEY]

        private_key = curve25519.Private()
        public_key = private_key.get_public()
        shared_key = private_key.get_shared_key(
            curve25519.Public(client_public),
            # Key is hashed before being returned, we don't want it; This fixes that.
            lambda x: x)

        mac = self._state.mac.encode()
        material = public_key.serialize() + mac + client_public
        server_proof = self._state.private_key.sign(material)

        output_key = hap_hkdf(shared_key, PVERIFY_1_SALT, PVERIFY_1_INFO)

        enc_context = {
            "client_public": client_public,
            "private_key": private_key,
            "public_key": public_key,
            "shared_key": shared_key,
            "pre_session_key": output_key
        }

        message = tlv.encode(HAP_TLV_TAGS.USERNAME, mac,
                             HAP_TLV_TAGS.PROOF, server_proof)

        cipher = CHACHA20_POLY1305(output_key, "python")
        aead_message = bytes(
            cipher.seal(PVERIFY_1_NONCE, bytearray(message), b""))
        data = tlv.encode(HAP_TLV_TAGS.SEQUENCE_NUM, b'\x02',
                          HAP_TLV_TAGS.ENCRYPTED_DATA, aead_message,
                          HAP_TLV_TAGS.PUBLIC_KEY, public_key.serialize())
        return data, enc_context

    def _pair_verify_two(self, tlv_objects, enc_context):
        """Verify the client proof and upgrade to encrypted transport.

        @param tlv_objects: The TLV data received from the client.
        @type tlv_object: dict
        """
        logging.debug('Pair verify [2/2]')
        encrypted_data = tlv_objects[HAP_TLV_TAGS.ENCRYPTED_DATA]
        cipher = CHACHA20_POLY1305(enc_context['pre_session_key'], 'python')
        decrypted_data = cipher.open(PVERIFY_2_NONCE, bytearray(encrypted_data), b'')
        assert decrypted_data is not None  # TODO:

        dec_tlv_objects = tlv.decode(bytes(decrypted_data))
        client_username = dec_tlv_objects[HAP_TLV_TAGS.USERNAME]
        material = enc_context['client_public'] \
            + client_username \
            + enc_context['public_key'].serialize()

        client_uuid = uuid.UUID(str(client_username, 'ascii'))
        perm_client_public = self._state.paired_clients.get(client_uuid)
        if perm_client_public is None:
            logging.debug('Client %s attempted pair verify without being paired first.',
                          client_uuid)
            return tlv.encode(HAP_TLV_TAGS.ERROR_CODE, HAP_OPERATION_CODE.INVALID_REQUEST)

        verifying_key = ed25519.VerifyingKey(perm_client_public)
        try:
            verifying_key.verify(dec_tlv_objects[HAP_TLV_TAGS.PROOF], material)
        except ed25519.BadSignatureError:
            logging.error('Bad signature, abort.')
            return tlv.encode(HAP_TLV_TAGS.ERROR_CODE, HAP_OPERATION_CODE.INVALID_REQUEST)

        return tlv.encode(HAP_TLV_TAGS.SEQUENCE_NUM, b'\x04'), None

    def _handle_accessories(self):
        hap_rep = self._accessory_driver.get_accessories()
        return json.dumps(hap_rep).encode('utf-8')

    def _handle_get_characteristics(self, query_dict):
        chars = self._accessory_driver.get_characteristics(query_dict["id"][0].split(","))
        return json.dumps(chars).encode("utf-8")

    def _handle_pairings(self, indata):
        tlv_objects = tlv.decode(indata)
        request_type = tlv_objects[HAP_TLV_TAGS.REQUEST_TYPE][0]
        if request_type == 3:
            return self._handle_add_pairing(tlv_objects)
        elif request_type == 4:
            return self._handle_remove_pairing(tlv_objects)
        else:
            raise ValueError

    def _handle_add_pairing(self, tlv_objects):
        """Update client information."""
        logging.debug('Adding client pairing.')
        client_username = tlv_objects[HAP_TLV_TAGS.USERNAME]
        client_public = tlv_objects[HAP_TLV_TAGS.PUBLIC_KEY]
        client_uuid = uuid.UUID(str(client_username, "utf-8"))
        should_confirm = self._accessory_driver.pair(
            client_uuid, client_public)
        if not should_confirm:
            self.send_response(500)
            return

        return tlv.encode(HAP_TLV_TAGS.SEQUENCE_NUM, b"\x02")

    def _handle_remove_pairing(self, tlv_objects):
        """Remove pairing with the client."""
        logging.debug('Removing client pairing.')
        client_username = tlv_objects[HAP_TLV_TAGS.USERNAME]
        client_uuid = uuid.UUID(str(client_username, "utf-8"))
        self._accessory_driver.unpair(client_uuid)

        return tlv.encode(HAP_TLV_TAGS.SEQUENCE_NUM, b"\x02")
