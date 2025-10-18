from passlib.context import CryptContext



pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')


def hash(pwd:str):
    return pwd_context.hash(pwd)


def verify(userPwd, hashedPwd):
    return pwd_context.verify(userPwd, hashedPwd)







