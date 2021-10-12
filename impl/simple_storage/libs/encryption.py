import json
import base64
import time
import hashlib
from Crypto.Cipher import AES
from Crypto import Random

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


def encrypt(data, bytes_key):
    data = pad(data)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(bytes_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(data.encode()))


def decrypt(enc_data, bytes_key):
    enc_data = base64.b64decode(enc_data)
    iv = enc_data[:16]
    cipher = AES.new(bytes_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc_data[16:]))
