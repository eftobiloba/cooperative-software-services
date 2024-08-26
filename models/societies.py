from pydantic import BaseModel, Field
from typing import Optional, List

class Society(BaseModel):
    society_id: str = Field(unique=True)
    society_name: str
    address: Optional[str]
    payment_plan: str
    forms: Optional[List[str]]
    actions: Optional[List[str]]