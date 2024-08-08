from pydantic import BaseModel
from datetime import datetime

class Repayment(BaseModel):
    loan_transaction_id: str
    amount: float
    date: datetime