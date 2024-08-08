from pydantic import BaseModel
from typing import List, Optional
from models.members import Beneficiary, PersonalInfo, CorporateWorkInfo, SelfEmployedWorkInfo, BankDetails, Expenses


class NonMember(BaseModel):
    non_member_id: str
    personal_info: Optional[PersonalInfo] = None
    beneficiaries: Optional[List[Beneficiary]] = None
    corporate_work_info: Optional[List[CorporateWorkInfo]] = None
    self_employed_work_info: Optional[List[SelfEmployedWorkInfo]] = None
    bank_details: Optional[List[BankDetails]] = None
    expenses: Optional[List[Expenses]] = None
