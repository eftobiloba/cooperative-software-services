from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class SavingsTransaction(BaseModel):
    membership_no: str
    email: Optional[str] = None
    transref: str
    product_id: str
    society_id: str
    timestamp: datetime
    description: str
    type: str
    amount: float
    status: str = "pending"
    formonth: Optional[str] = None

class SavingsProduct(BaseModel):
    product_id: str
    product_name: str
    description: str
    society_id: str
    minimum_saveable: float
    minimum_untouchable: float
    interest_return: float
    required_info: List[str]

class SavingsBalance(BaseModel):
    membership_no: str
    product_id: str
    society_id: str
    balance: float