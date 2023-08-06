import hashlib, binascii, os
from cryptography.fernet import Fernet

def encrypt(secret_key, data):
    if type(secret_key) == str: secret_key = bytes(secret_key, "utf-8")
    if type(data) == str: data = bytes(data, "utf-8")
    return Fernet(secret_key).encrypt(data)

def decrypt(secret_key, data):
    if type(secret_key) == str: secret_key = bytes(secret_key, "utf-8")
    if type(data) == str: data = bytes(data, "utf-8")
    return Fernet(secret_key).decrypt(data)

def generateSecretKey():
    return Fernet.generate_key()

def hashText(text):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', text.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verifyHash(hash, text):
    salt = hash[:64]
    hash = hash[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', text.encode('utf-8'), salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == hash
