from models.members import *
from typing import List

def address_serial(address: Address) -> dict:
    return {
        "country": address.country,
        "state": address.state,
        "lga": address.lga,
        "street": address.street,
        "house_color": address.house_color
    }

def list_address_serial(addresses: List[Address]) -> list:
    return [address_serial(address) for address in addresses]

def beneficiary_serial(beneficiary: Beneficiary) -> dict:
    return {
        "name": beneficiary.name,
        "relationship": beneficiary.relationship,
        "age": beneficiary.age,
        "telephone": beneficiary.telephone,
        "address": list_address_serial(beneficiary.address) if beneficiary.address else None
    }

def list_beneficiary_serial(beneficiaries: List[Beneficiary]) -> list:
    return [beneficiary_serial(beneficiary) for beneficiary in beneficiaries]

def personal_info_serial(personal_info: PersonalInfo) -> dict:
    return {
        "first_name": personal_info.first_name,
        "last_name": personal_info.last_name,
        "address": list_address_serial(personal_info.address) if personal_info.address else None,
        "dob": personal_info.dob.isoformat() if personal_info.dob else None,
        "telephone": personal_info.telephone,
        "email": personal_info.email,
        "gender": personal_info.gender
    }

def corporate_work_info_serial(cwi: CorporateWorkInfo) -> dict:
    return {
        "job_type": cwi.job_type,
        "job_title": cwi.job_title,
        "company_name": cwi.company_name,
        "company_address": cwi.company_address,
        "length_of_employment": cwi.length_of_employment,
        "date_started": cwi.date_started,
        "date_ended": cwi.date_ended,
        "net_monthly_pay": cwi.net_monthly_pay,
        "supervisor_name": cwi.supervisor_name,
        "supervisor_phone": cwi.supervisor_phone
    }

def list_corporate_work_info_serial(cwis: List[CorporateWorkInfo]) -> list:
    return [corporate_work_info_serial(cwi) for cwi in cwis]

def self_employed_work_info_serial(sewi: SelfEmployedWorkInfo) -> dict:
    return {
        "job_type": sewi.job_type,
        "business_name": sewi.business_name,
        "average_daily_income": sewi.average_daily_income,
        "date_started": sewi.date_started,
        "date_ended": sewi.date_ended
    }

def list_self_employed_work_info_serial(sewis: List[SelfEmployedWorkInfo]) -> list:
    return [self_employed_work_info_serial(sewi) for sewi in sewis]

def bank_details_serial(bank_detail: BankDetails) -> dict:
    return {
        "account_name": bank_detail.account_name,
        "account_number": bank_detail.account_number,
        "bank_name": bank_detail.bank_name,
        "bank_address": bank_detail.bank_address,
        "current_account": bank_detail.current_account,
        "account_officer": bank_detail.account_officer
    }

def list_bank_details_serial(bank_details: List[BankDetails]) -> list:
    return [bank_details_serial(bank_detail) for bank_detail in bank_details]

def expenses_serial(expenses: Expenses) -> dict:
    return {
        "mortgage_amount": expenses.mortgage_amount,
        "rent_amount": expenses.rent_amount,
        "motor_lease_amount": expenses.motor_lease_amount,
        "general_maintenance": expenses.general_maintenance,
        "child_care": expenses.child_care
    }

def list_expenses_serial(expenses_list: List[Expenses]) -> list:
    return [expenses_serial(expenses) for expenses in expenses_list]

def cooperative_info_serial(coop_info: CooperativeInfo) -> dict:
    return {
        "membership_no": coop_info.membership_no,
        "society_id": coop_info.society_id,
        "date_joined": coop_info.date_joined.isoformat() if coop_info.date_joined else None
    }

def member_serial(member: Member) -> dict:
    return {
        "cooperative_info": cooperative_info_serial(member.cooperative_info),
        "personal_info": personal_info_serial(member.personal_info) if member.personal_info else None,
        "beneficiaries": list_beneficiary_serial(member.beneficiaries) if member.beneficiaries else None,
        "corporate_work_info": list_corporate_work_info_serial(member.corporate_work_info) if member.corporate_work_info else None,
        "self_employed_work_info": list_self_employed_work_info_serial(member.self_employed_work_info) if member.self_employed_work_info else None,
        "bank_details": list_bank_details_serial(member.bank_details) if member.bank_details else None,
        "expenses": list_expenses_serial(member.expenses) if member.expenses else None,
        "password": member.password
    }

def list_member_serial(members: List[Member]) -> list:
    return [member_serial(member) for member in members]