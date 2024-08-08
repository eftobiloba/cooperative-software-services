from pydantic import BaseModel

class Admin(BaseModel):
    admin_id: str
    society_id: str
    username: str
    first_name: str
    last_name: str
    password: str
    access_type: str = "super"
    
class Token(BaseModel):
    access_token: str
    token_type: str