from models.admins import Admin
from models.societies import Society

def admin_serial(admin: Admin) -> dict:
    return{
        "admin_id": admin["admin_id"],
        "society_id": admin["society_id"],
        "username": admin["username"],
        "first_name": admin["first_name"],
        "last_name": admin["last_name"],
        "password": admin["password"],
        "access_type": admin["access_type"],
    }

def list_admin_serial(admins) -> list:
    return [admin_serial(admin) for admin in admins]


def society_serial(society: Society) -> dict:
    return{
        "society_id": society["society_id"],
        "society_name": society["society_name"],
        "staff_number": society["staff_number"],
        "address": society["address"],
        "member_number": society["member_number"],
        "payment_plan": society["payment_plan"],
    }

def list_society_serial(societies) -> list:
    return [society_serial(society) for society in societies]