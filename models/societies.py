from pydantic import BaseModel, Field
from typing import Optional

class Society(BaseModel):
    society_id: str = Field(unique=True)
    society_name: str
    staff_number: int
    address: Optional[str]
    member_number: int
    payment_plan: str