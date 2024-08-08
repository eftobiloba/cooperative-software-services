from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LoanTransaction(BaseModel):
    membership_no: Optional[str] = None
    non_member_id: Optional[str] = None
    email: Optional[str] = None
    transref: str
    product_id: str
    society_id: str
    timestamp: datetime
    calculation_method: str
    loantype: str
    interest: float
    amount: float
    period: int
    status: str = "pending"
    completed: bool = False
    date_approved: datetime

class LoanProduct(BaseModel):
    product_id: str
    product_name: str
    description: str
    society_id: str
    interest: float
    calculation_method: str
    form_id: Optional[str]