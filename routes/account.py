from typing import Annotated
from fastapi import APIRouter, Depends
from models.members import *
from models.nonmembers import NonMember
from schemas.members import *
from schemas.nonmembers import *
from schemas.transactions import *
from modules.account.oauth import get_current_user
from config.database import *

account_router = APIRouter()

@account_router.get("/me", response_model = Member)
async def read_root(current_user: Annotated[Member, Depends(get_current_user)]):
	return current_user

@account_router.get("/balance/all")
async def read_all_balance(current_user: Annotated[Member, Depends(get_current_user)]):
	current_active_user = member_serial(current_user)
	membership_no = current_active_user["membership_no"]
	balances = list_savings_balance_serial(balance_collection.find({"cooperative_info.membership_no": membership_no}))
    
	if balances:
		return {"code": "00", "message": "success", "data": balances}
	else:
		return {"code": "01", "message": "failure", "data": "no balances"}

@account_router.get("/balance/one/{product_id}")
async def read_product_balance(product_id: str, current_user: Annotated[Member, Depends(get_current_user)]):
	current_active_user = member_serial(current_user)
	membership_no = current_active_user["membership_no"]
	balances = list_savings_balance_serial(balance_collection.find({"membership_no": membership_no, "product_id": product_id}))
    
	if balances:
		return {"code": "00", "message": "success", "data": balances}
	else:
		return {"code": "01", "message": "failure", "data": "no balances"}
	