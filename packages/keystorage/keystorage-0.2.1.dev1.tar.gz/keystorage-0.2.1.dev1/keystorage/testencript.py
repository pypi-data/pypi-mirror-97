import base64
import hashlib

from Crypto import Random
from Crypto import Cipher
from Crypto.Cipher import AES


key = hashlib.sha256(b"fraco").hexdigest()[:32]
print(key, len(key))
cipher = AES.new(key)

ciphertext = cipher.encrypt("francisco cñvaj")
print(ciphertext, len(ciphertext))

plaintext = cipher.decrypt(ciphertext)
print(plaintext)

