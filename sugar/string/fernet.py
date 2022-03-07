"""
FERNET - safe encryption / decryption utility
2020 (c) OrangeShine, Inc.
"""
from cryptography.fernet import Fernet
from .base64 import to_bytes
from .base64 import base64_decode


class FernetHandler(object):
    def __init__(self, key=""):
        if key:
            self.cipher_suite = Fernet(to_bytes(key))
        else:
            self.cipher_suite = None

    @staticmethod
    def generate_key():
        return Fernet.generate_key().decode('utf-8')

    def encrypt(self, text=""):
        if text and self.cipher_suite:
            try:
                return self.cipher_suite.encrypt(
                    to_bytes(text)).decode('utf-8')
            except:
                pass
        return ""

    def encrypt_to_bytes(self, text=""):
        if text and self.cipher_suite:
            try:
                return self.cipher_suite.encrypt(to_bytes(text))
            except Exception as e:
                print("%s %s" % (str(type(e)), str(e)))
                pass
        return ""

    def decrypt(self, encrypted=""):
        if encrypted and self.cipher_suite:
            try:
                decr = self.cipher_suite.decrypt(
                    to_bytes(encrypted)).decode('utf-8')
                if encrypted != decr:
                    return decr
                else:
                    return base64_decode(encrypted)
            except:
                try:
                    return base64_decode(encrypted)
                except:
                    pass
        return encrypted


# if __name__ == '__main__':
#     from utility.string.base64 import base64_decode, base64_encode, to_bytes
#     from utility.string.fernet import FernetHandler
#
#     f_key = FernetHandler().generate_key()
#     fh = FernetHandler(f_key)
#     test_str = "this is a test!!"
#     test_str_bytes = to_bytes(test_str)
#     encrypted_str = fh.encrypt(test_str)
#     decrypted_str = fh.decrypt(encrypted_str)
#     encoded_str = base64_encode(test_str)
#     decoded_str = base64_decode(encoded_str)
#
#     print("#################################")
#     print("[debug] f_key = %s" % f_key)
#     print("[debug] test_str: %s" % test_str)
#     print("[debug] test_str_bytes: %s" % test_str_bytes)
#     print("[debug] encoded_str: %s" % encoded_str)
#     print("[debug] decoded_str: %s" % decoded_str)
#     print("[debug] encrypted_str: %s" % encrypted_str)
#     print("[debug] decrypted_str: %s" % decrypted_str)
#     print("#################################")
