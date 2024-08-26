from pydantic import BaseModel
from typing import Optional

class Admin(BaseModel):
    admin_id: str
    society_id: str
    username: Optional[str] = ""
    first_name: str
    last_name: str
    password: str
    access_type: str = "super"
    
class Token(BaseModel):
    access_token: str
    token_type: str