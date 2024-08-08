from datetime import datetime, timedelta
from jose import JWTError, jwt
from models import members
from config.database import member_collection
from config.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        membership_no: str = payload.get("sub")
        if membership_no is None:
            raise credentials_exception
        token_data = members.TokenData(membership_no=membership_no)
        
    except JWTError:
        raise credentials_exception
    
    member = member_collection.find_one({"cooperative_info.membership_no": membership_no})
    if member is None:
        raise credentials_exception
    return member