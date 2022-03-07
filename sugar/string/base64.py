"""
base64 - safe encoding / decoding utility
2020 (c) OrangeShine, Inc.
"""
import base64


def to_bytes(text=""):
    return text if isinstance(text, bytes) else text.encode('utf-8')


def base64_decode(encoded=""):
    if encoded:
        try:
            return base64.b64decode(to_bytes(encoded)).decode('utf-8')
        except:
            pass
    return encoded


def base64_encode(text=""):
    if text:
        try:
            return base64.b64encode(to_bytes(text)).decode('utf-8')
        except:
            pass
    return ""


# if __name__ == '__main__':
#     from utility.string.base64 import base64_decode, base64_encode, to_bytes
#     # from utility.string.fernet import FernetHandler
#
#     # f_key = FernetHandler().generate_key()
#     # fh = FernetHandler(f_key)
#     test_str = "this is a test!!"
#     test_str_bytes = to_bytes(test_str)
#     # encrypted_str = fh.encrypt(test_str)
#
#     encoded_str = base64_encode(test_str)
#     decoded_str = base64_decode(encoded_str)
#     # wrong_decoded_str = base64_decode(encrypted_str)
#
#     print("#################################")
#     # print("[debug] f_key = %s" % f_key)
#     print("[debug] test_str: %s" % test_str)
#     print("[debug] test_str_bytes: %s" % test_str_bytes)
#     print("[debug] encoded_str: %s" % encoded_str)
#     print("[debug] decoded_str: %s" % decoded_str)
#     # print("[debug] encrypted_str: %s" % encrypted_str)
#     # print("[debug] wrong_decoded_str: %s" % wrong_decoded_str)
#     print("#################################")
