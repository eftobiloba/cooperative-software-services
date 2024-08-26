from typing import Annotated, List
from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from models.admins import Admin
from models.devs import Developer
from models.savings import SavingsTransaction
from models.members import Member
from modules.security import passwordSSH
from config.database import *
from models.forms import Action, Form, FormInDB, form_helper
from schemas.developers import *
from schemas.actions import *
from schemas.societies import admin_serial
from schemas.members import *
from schemas.transactions import savings_transaction_serial, list_savings_transaction_serial

dev_router = APIRouter()

def get_dev_data(access_token: str):
    dev_data = dev_collection.find_one({"dev_access_token": access_token})
    if dev_data:
        return developer_serial(dev_data)
    else:
        return {}
    
def verify_access_token(access_token: str):
    dev_data = dev_collection.find_one({"dev_access_token": access_token})
    if dev_data:
        return True
    else:
        return False

@dev_router.post('/register')
async def register_developer(request: Developer):
    hashed_pass = passwordSSH.hash_password(request.password)
    dev_object = dict(request)
    dev_object["password"] = hashed_pass
    dev_object["status"] = "pending"
    dev_collection.insert_one(dev_object)
    return {"code": "00", "message": "success", "data": "Registration successful, we'll get back to you via your email!"}

@dev_router.get('/access-token/{developer_id}')
async def get_access_token(developer_id: str):
    dev_data = developer_serial(dev_collection.find_one({"dev_id": developer_id}))
    if dev_data:
        return {"code": "00", "message": "success", "data": dev_data["dev_access_token"]}
    else:
        return {"code": "01", "message": "failure", "data": "Invalid developer ID"}

@dev_router.get('/{access_token}/actions/')
async def get_all_dev_actions(access_token: str):
    developer_data = get_dev_data(access_token)
    if not developer_data:
        return {"code": "01", "message": "failure", "data": "Invalid access token or no developer data found"}
    
    developer_id = developer_data.get("dev_id")
    actions = actions_collection.find({"developer_id": developer_id})
    actions = list_actions_serial(actions)
    if actions:
        return {"code": "00", "message": "success", "data": actions}
    else:
        return {"code": "01", "message": "failure", "data": "No actions found"}
    
@dev_router.get('/{access_token}/actions/one/{action_id}')
async def get_one_dev_actions(access_token: str, action_id: str):
    developer_data = get_dev_data(access_token)
    if not developer_data:
        return {"code": "01", "message": "failure", "data": "Invalid access token or no developer data found"}
    
    developer_id = developer_data.get("dev_id")
    action = actions_collection.find({"developer_id": developer_id, "action_id": action_id})
    action = action_serial(action)
    if action:
        return {"code": "00", "message": "success", "data": action}
    else:
        return {"code": "01", "message": "failure", "data": "No action found"}
    
@dev_router.get('/{access_token}/forms/')
async def get_all_dev_forms(access_token: str):
    developer_data = get_dev_data(access_token)
    if not developer_data:
        return {"code": "01", "message": "failure", "data": "Invalid access token or no developer data found"}
    
    developer_id = developer_data.get("dev_id")
    forms = forms_collection.find({"developer_id": developer_id})
    forms = list_actions_serial(forms)
    if forms:
        return {"code": "00", "message": "success", "data": [form_helper(form) for form in forms]}
    else:
        return {"code": "01", "message": "failure", "data": "You have not created any forms"}

@dev_router.get('/{access_token}/forms/one/{form_id}')
async def get_one_dev_form(access_token: str, form_id: str):
    developer_data = get_dev_data(access_token)
    if not developer_data:
        return {"code": "01", "message": "failure", "data": "Invalid access token or no developer data found"}
    
    developer_id = developer_data["developer_id"]
    form = forms_collection.find_one({"developer_id": developer_id, "form_id": form_id})
    if form:
        return {"code": "00", "message": "success", "data": form_helper(form)}
    else:
        return {"code": "01", "message": "failure", "data": "Form not found"}

@dev_router.post("/{access_token}/forms/", response_model=FormInDB)
async def dev_create_form(form: Form, access_token: str):
    developer_data = get_dev_data(access_token)
    developer_id = developer_data["developer_id"]
    form_dict = dict(form)
    form["developer_id"] = developer_id
    result = forms_collection.insert_one(form_dict)
    new_form = forms_collection.find_one({"_id": result.inserted_id})
    return form_helper(new_form)

## Get all transactions
@dev_router.get("/{access_token}/savings/{society_id}/{product_id}/")
async def get_savings_transactions(access_token: str, society_id: str, product_id: str):
    if (verify_access_token(access_token)):
        transactions = list_savings_transaction_serial(savings_transactions_collection.find({"society_id": society_id, "product_id": product_id}))
        if transactions:
            return {"code": "00", "message": "success", "data": transactions}
        else:
            return {"code": "01", "message": "failure", "data": "No transactions found"}
    else:
        return {"code": "99", "message": "error", "data": "Not authenticated"}

## Get a transaction detail
@dev_router.get("/{access_token}/savings/{transaction_id}/")
async def get_savings_transaction(access_token: str, transaction_id: str):
    if (verify_access_token(access_token)):
        transaction = savings_transactions_collection.find_one({"_id": ObjectId(transaction_id)})
        if transaction:
            return {"code": "00", "message": "success", "data": savings_transaction_serial(transaction)}
        else:
            return {"code": "01", "message": "failure", "data": "No transactions found"}
    else:
        return {"code": "99", "message": "error", "data": "Not authenticated"}
    
## Create new savings transaction
@dev_router.post("/{access_token}/savings/{society_id}/{product_id}/")
async def add_savings_transaction(access_token: str, transaction: SavingsTransaction):
    if (verify_access_token(access_token)):
        savings_transactions_collection.insert_one(dict(transaction))
        return {"code": "00", "message": "success", "data": "Transaction successfully added"}
    else:
        return {"code": "99", "message": "error", "data": "Not authenticated"}

## Delete a transaction
@dev_router.delete("/{access_token}/savings/{transaction_id}/")
async def delete_savings_transaction(access_token: str, transaction_id: str):
    if (verify_access_token(access_token)):
        delete_result = savings_transactions_collection.delete_one({"_id": ObjectId(transaction_id)})
        deleted_count = delete_result.deleted_count
        if deleted_count == 1:
            return {"code": "00", "message": "success", "data": "Transaction successfully deleted"}
        else:
            return {"code": "01", "message": "failure", "data": "Transaction not found"}
    else:
        return {"code": "99", "message": "error", "data": "Not authenticated"}
    
# Update a transaction's information
@dev_router.put("/{access_token}/savings/{transaction_id}/")
async def update_transactions(access_token: str, transaction_id: str, transaction: SavingsTransaction):
    if (verify_access_token(access_token)):
        updated_transaction = savings_transactions_collection.find_one_and_update({"_id": ObjectId(transaction_id)}, {"$set":dict(transaction)})
        if updated_transaction:
            return {"code": "00", "message": "success", "data": "Transaction successfully updated"}
        else:
            return {"code": "01", "message": "failure", "data": "Transaction not found"}
    else:
        return {"code": "99", "message": "failure", "error": "Not authenticated"}
    
@dev_router.get("/admins/{username}")
async def get_admin(username: str):
    admin = admin_collection.find_one({"username": username})
    return admin

# Add new member to the db
@dev_router.post("/{access_token}/members/", status_code=status.HTTP_201_CREATED)
async def create_member(access_token: str, member: Member):
    if (verify_access_token(access_token)):
        if member_collection.find_one({"cooperative_info.membership_no": member.cooperative_info.membership_no}):
            raise HTTPException(status_code=400, detail="Member with this membership number already exists.")
        member_collection.insert_one(member.dict())
        return {"code": "00", "message": "success", "data": "Member successfully added"}
    else:
        return {"code": "99", "message": "failure", "error": "Not authenticated"}

# Retrieve a member by ID
@dev_router.get("/{access_token}/members/{member_id}", response_model=Member)
async def get_member(access_token: str, member_id: str):
    if (verify_access_token(access_token)):
        member = member_collection.find_one({"_id": ObjectId(member_id)})
        if not member:
            raise HTTPException(status_code=404, detail="Member not found.")
        return {"code": "00", "message": "success", "data": member}
    else:
        return {"code": "99", "message": "failure", "error": "Not authenticated"}

# Retrieve all members
@dev_router.get("/{access_token}/members/{society_id}/", response_model=List[Member])
async def get_all_members(access_token: str, society_id: str):
    if (verify_access_token(access_token)):
        members = member_collection.find({"cooperative_info.society_id": society_id})
        return [list_member_serial(members)]
    else:
        return {"code": "99", "message": "failure", "error": "Not authenticated"}

# Update a member
@dev_router.put("/{access_token}/members/{member_id}", response_model=Member)
async def update_member(access_token: str, member_id: str, updated_member: Member):
    if (verify_access_token(access_token)):
        member = member_collection.find_one({"_id": ObjectId(member_id)})
        if not member:
            raise HTTPException(status_code=404, detail="Member not found.")
        
        updated_member_dict = updated_member.dict(exclude_unset=True)
        member_collection.update_one({"_id": ObjectId(member_id)}, {"$set": updated_member_dict})
        return {"code": "00", "message": "success", "data": "Member successfully deleted"}
    else:
        return {"code": "99", "message": "failure", "error": "Not authenticated"}

# Delete a member
@dev_router.delete("/{access_token}/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_member(access_token: str, member_id: str):
    if (verify_access_token(access_token)):
        member = member_collection.find_one({"_id": ObjectId(member_id)})
        if not member:
            raise HTTPException(status_code=404, detail="Member not found.")
        member_collection.delete_one({"_id": ObjectId(member_id)})
        {"code": "00", "message": "success", "data": "Member successfully deleted"}
    else:
        return {"code": "99", "message": "failure", "error": "Not authenticated"}