from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

class Address(BaseModel):
    country: str
    state: str
    lga: str
    street: str
    house_color: Optional[str] = None

class Beneficiary(BaseModel):
    name: str
    relationship: str
    age: int
    telephone: str
    address: Optional[List[Address]] = None

class PersonalInfo(BaseModel):
    first_name: str
    last_name: str
    address: Optional[List[Address]] = None
    dob: Optional[datetime] = None
    telephone: str
    email: Optional[EmailStr] = None
    gender: Optional[str] = None

class CorporateWorkInfo(BaseModel):
    job_type: str
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    company_address: Optional[str] = None
    length_of_employment: Optional[str] = None
    date_started: Optional[str] = None
    date_ended: Optional[str] = None
    net_monthly_pay: Optional[float] = None
    supervisor_name: Optional[str] = None
    supervisor_phone: Optional[str] = None

class SelfEmployedWorkInfo(BaseModel):
    job_type: str
    business_name: Optional[str] = None
    average_daily_income: Optional[float] = None
    date_started: Optional[str] = None
    date_ended: Optional[str] = None

class BankDetails(BaseModel):
    account_name: str
    account_number: str
    bank_name: str
    bank_address: Optional[str] = None
    current_account: Optional[str] = None
    account_officer: Optional[str] = None

class Expenses(BaseModel):
    mortgage_amount: Optional[float] = None
    rent_amount: Optional[float] = None
    motor_lease_amount: Optional[float] = None
    general_maintenance: Optional[float] = None
    child_care: Optional[float] = None

class CooperativeInfo(BaseModel):
    membership_no: str = Field(unique=True)
    society_id: str
    date_joined: Optional[datetime] = None

class Member(BaseModel):
    cooperative_info: CooperativeInfo
    personal_info: Optional[PersonalInfo] = None
    beneficiaries: Optional[List[Beneficiary]] = None
    corporate_work_info: Optional[List[CorporateWorkInfo]] = None
    self_employed_work_info: Optional[List[SelfEmployedWorkInfo]] = None
    bank_details: Optional[List[BankDetails]] = None
    expenses: Optional[List[Expenses]] = None
    password: str

class Login(BaseModel):
    membership_no: str
    society_id: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    membership_no: Optional[str] = None