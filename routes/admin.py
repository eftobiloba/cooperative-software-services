from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from config.database import *
from modules.security import passwordSSH
from modules.admin_account import jwttoken
from models.admins import Token, Admin
from modules.admin_account.oauth import get_current_admin
from schemas.members import *
from schemas.societies import *
from schemas.transactions import *

admin_router = APIRouter()

@admin_router.post('/login')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    admin = admin_collection.find_one({"email": form_data.username})

    if not admin:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not passwordSSH.verify_password(admin["password"], form_data.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    access_token = jwttoken.create_access_token(data={"sub": admin["email"]})

    return Token(access_token=access_token, token_type="bearer")

@admin_router.get("/me", response_model = Admin)
async def read_root(current_admin: Annotated[Admin, Depends(get_current_admin)]):
	return current_admin

@admin_router.get('/members')
async def all_members(current_admin: Annotated[Admin, Depends(get_current_admin)]):
    current_active_admin = admin_serial(current_admin)
    society_id = current_active_admin["society_id"]
    members = list_member_serial(member_collection.find({"cooperative_info.society_id": society_id}))
    if members:
        return {"code": "00", "message": "success", "data": members}
    else:
        return {"code": "01", "message": "not found", "data": members}
    
@admin_router.get("/members/one/{membership_no}")
async def get_member(membership_no: str, current_admin: Annotated[Admin, Depends(get_current_admin)]):
    current_active_admin = admin_serial(current_admin)
    society_id = current_active_admin["society_id"]
    member = member_collection.find_one({"cooperative_info.society_id": society_id, "cooperative_info.membership_no": membership_no}) 
    if member:
        return {"code": "00", "message": "success", "data": member_serial(member)}
    else:
        return {"code": "01", "message": "not found", "data": {}}
    
@admin_router.get("/members/one/balance/{membership_no}")
async def read_balance(membership_no: str, current_admin: Annotated[Admin, Depends(get_current_admin)]):
    current_active_admin = admin_serial(current_admin)
    society_id = current_active_admin["society_id"]
    balances = list_savings_balance_serial(balance_collection.find({"society_id": society_id, "membership_no": membership_no}))
    if balances:
        return {"code": "00", "message": "success", "data": balances}
    else:
        return {"code": "01", "message": "not found", "data": balances}

@admin_router.get("/members/savings/")
async def get_all_savings_transactions(current_admin: Annotated[Admin, Depends(get_current_admin)]):
    current_active_admin = admin_serial(current_admin)
    society_id = current_active_admin["society_id"]
    transactions = list_savings_transaction_serial(savings_transactions_collection.find({"society_id": society_id}))
    if transactions:
        return {"code": "00", "message": "success", "data": transactions}
    else:
        return {"code": "01", "message": "not found", "data": transactions}
    
@admin_router.get("/members/savings/{product_id}")
async def get_savings_transactions(product_id: str, current_admin: Annotated[Admin, Depends(get_current_admin)]):
    current_active_admin = admin_serial(current_admin)
    society_id = current_active_admin["society_id"]
    transactions = list_savings_transaction_serial(savings_transactions_collection.find({"society_id": society_id, "product_id": product_id}))
    if transactions:
        return {"code": "00", "message": "success", "data": transactions}
    else:
        return {"code": "01", "message": "not found", "data": transactions}

@admin_router.get("/members/one/savings/{product_id}/{membership_no}")
async def get_one_user_savings_transactions(membership_no: str, product_id: str, current_admin: Annotated[Admin, Depends(get_current_admin)]):
    current_active_admin = admin_serial(current_admin)
    society_id = current_active_admin["society_id"]
    transactions = list_savings_transaction_serial(savings_transactions_collection.find({"society_id": society_id, "membership_no": membership_no, "product_id": product_id}))
    if transactions:
        return {"code": "00", "message": "success", "data": transactions}
    else:
        return {"code": "01", "message": "not found", "data": transactions}

@admin_router.get("/members/one/savings/{membership_no}")
async def get_all_one_user_savings_transactions(membership_no: str, current_admin: Annotated[Admin, Depends(get_current_admin)]):
    current_active_admin = admin_serial(current_admin)
    society_id = current_active_admin["society_id"]
    transactions = list_savings_transaction_serial(savings_transactions_collection.find({"society_id": society_id, "membership_no": membership_no}))
    if transactions:
        return {"code": "00", "message": "success", "data": transactions}
    else:
        return {"code": "01", "message": "not found", "data": transactions}