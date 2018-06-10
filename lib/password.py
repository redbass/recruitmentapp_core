import bcrypt


def encrypt_password(password: str) -> str:
    password = bcrypt.hashpw(password.encode('utf-8'),
                             bcrypt.gensalt())
    return password.decode('utf-8')


def check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'),
                          hashed.encode('utf-8'))
