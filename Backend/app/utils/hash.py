from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_text(text: str):

    return pwd_context.hash(text)

def verify_text(text: str, hashed: str):

    return pwd_context.verify(text, hashed)