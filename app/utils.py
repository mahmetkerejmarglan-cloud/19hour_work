from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")



def hash(password:str):
    return pwd_context.hash(password)


def varify(plain_password, hashed_password):
    return pwd_context.verify(plain_password,hashed_password)