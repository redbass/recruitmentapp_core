import bcrypt
from Crypto.Cipher import AES


def encrypt_user_password(password: str) -> str:
    password = bcrypt.hashpw(password.encode('utf-8'),
                             bcrypt.gensalt())
    return password.decode('utf-8')


def check_user_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'),
                          hashed.encode('utf-8'))


def encrypt_system_password(password: str, enc_pwd: str, seed: str):
    aes = AES.new(enc_pwd, AES.MODE_CBC, seed)
    return aes.encrypt(password).hex()


def decrypt_system_password(cipher_hex: str, enc_pwd: str, seed: str):
    b_cipher_hex = bytes(bytearray.fromhex(cipher_hex))
    aes = AES.new(enc_pwd, AES.MODE_CBC, seed)
    return aes.decrypt(b_cipher_hex).decode()
