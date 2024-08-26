from pydantic import BaseModel
from typing import List, Optional

class Developer(BaseModel):
    dev_name: str
    dev_id: str
    dev_email: str
    dev_description: str
    dev_access_token: Optional[str] = ""
    actions: Optional[List[str]] = []
    forms: Optional[List[str]] = []
    status: Optional[str] = "pending"
    password: str