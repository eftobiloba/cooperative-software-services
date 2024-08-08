from models.members import *
from models.nonmembers import NonMember
from typing import List
from schemas.members import personal_info_serial, list_beneficiary_serial, list_corporate_work_info_serial, list_self_employed_work_info_serial, list_bank_details_serial, list_expenses_serial


def non_member_serial(nonmember: NonMember) -> dict:
    return {
        "non_member_id": nonmember.non_member_id,
        "personal_info": personal_info_serial(nonmember.personal_info) if nonmember.personal_info else None,
        "beneficiaries": list_beneficiary_serial(nonmember.beneficiaries) if nonmember.beneficiaries else None,
        "corporate_work_info": list_corporate_work_info_serial(nonmember.corporate_work_info) if nonmember.corporate_work_info else None,
        "self_employed_work_info": list_self_employed_work_info_serial(nonmember.self_employed_work_info) if nonmember.self_employed_work_info else None,
        "bank_details": list_bank_details_serial(nonmember.bank_details) if nonmember.bank_details else None,
        "expenses": list_expenses_serial(nonmember.expenses) if nonmember.expenses else None
    }

def list_non_member_serial(nonmembers: List[NonMember]) -> list:
    return [non_member_serial(nonmember) for nonmember in nonmembers]