from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from Crypto.Cipher import AES


class SimpleCrypto(object):
    def __init__(self):
        self.secret_key = '1234567890123456'
        self.cipher = AES.new(self.secret_key, AES.MODE_ECB)

    def encrypt(self, msg):
        msg_text = msg.rjust(96)
        return urlsafe_base64_encode(self.cipher.encrypt(msg_text)).decode('utf-8')

    def decrypt(self, encoded):
        decoded = self.cipher.decrypt(urlsafe_base64_decode(encoded))
        return decoded.strip().decode('utf-8')
