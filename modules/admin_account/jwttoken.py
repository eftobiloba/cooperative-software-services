from datetime import datetime, timedelta
from jose import JWTError, jwt
from config.database import admin_collection
from config.config import ADMIN_SECRET_KEY, ALGORITHM, ADMIN_ACCESS_TOKEN_EXPIRE_MINUTES



def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ADMIN_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, ADMIN_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token, ADMIN_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    
    admin = admin_collection.find_one({"username": username})
    if admin is None:
        raise credentials_exception
    return admin