from datetime import timedelta, datetime
import jwt

secret_key = "0943lds0o98icjo34kr39fucvoi3n4lkjrf09sd8iocjvl3k4t0f98dusj3kl"
algorithm = "HS256"



def create_access_token(*, data:dict, expires_delta: timedelta=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

def decode_access_token(*, data: str):
    to_decode = data
    return jwt.decode(to_decode, secret_key, algorithm=algorithm)
