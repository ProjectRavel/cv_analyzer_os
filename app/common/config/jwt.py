from jose import JWTError, jwt
from datetime import datetime, timedelta

# secret key (nanti masuk ke .env)
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"


# making acces token when user login
def create_acces_token(data: dict, expires_delta: timedelta = None):
    try:
        # copy data to encode
        to_encode = data.copy()

        # set expiration time for the token, default 1 hour
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=1)

        to_encode.update({"exp": expire})

    except Exception as e:
        raise ValueError("Error occurred while encoding JWT", str(e))

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
