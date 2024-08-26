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
from models.forms import FormInDB, Form, form_helper, FormSubmission
from bson import ObjectId

admin_router = APIRouter()

@admin_router.get("/societies")
async def get_societies():
    societies = list_society_serial(society_collection.find())
    return societies

@admin_router.post('/login')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    admin = admin_collection.find_one({"username": form_data.username})

    if not admin:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not passwordSSH.verify_password(admin["password"], form_data.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    access_token = jwttoken.create_access_token(data={"sub": admin["username"]})

    return Token(access_token=access_token, token_type="bearer")

@admin_router.get("/me", response_model = Admin)
async def read_root(current_admin: Annotated[Admin, Depends(get_current_admin)]):
	return current_admin

# Create a new form
@admin_router.post("/forms/", response_model=FormInDB)
async def create_form(form: Form, current_admin: Annotated[Admin, Depends(get_current_admin)]):
    current_active_admin = admin_serial(current_admin)
    form_dict = form.dict()
    form["society_id"] = current_active_admin["society_id"]
    result = forms_collection.insert_one(form_dict)
    new_form = forms_collection.find_one({"_id": result.inserted_id})
    return form_helper(new_form)

# Get a form by ID
@admin_router.get("/forms/{form_id}", response_model=FormInDB)
async def get_form(form_id: str, current_admin: Annotated[Admin, Depends(get_current_admin)]):
    current_active_admin = admin_serial(current_admin)
    form = forms_collection.find_one({"form_id": form_id, "society_id": current_active_admin["society_id"]})
    if form is None:
        raise HTTPException(status_code=404, detail="Form not found")
    return form_helper(form)

# Get all forms
@admin_router.get("/forms/", response_model=List[FormInDB])
async def get_all_forms(current_admin: Annotated[Admin, Depends(get_current_admin)]):
    current_active_admin = admin_serial(current_admin)
    forms = forms_collection.find({"society_id": current_active_admin["society_id"]})
    return [form_helper(form) for form in forms]

# Update a form by ID
@admin_router.put("/forms/{form_id}", response_model=FormInDB)
async def update_form(form_id: str, updated_form: Form, current_admin: Annotated[Admin, Depends(get_current_admin)]):
    current_active_admin = admin_serial(current_admin)
    result = forms_collection.update_one({"form_id": form_id, "society_id": current_active_admin["society_id"]})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Form not found")
    updated_form = forms_collection.find_one({"_id": ObjectId(form_id)})
    return form_helper(updated_form)

# Delete a form by ID
@admin_router.delete("/forms/{form_id}")
async def delete_form(form_id: str, current_admin: Annotated[Admin, Depends(get_current_admin)]):
    current_active_admin = admin_serial(current_admin)
    result = forms_collection.delete_one({"form_id": form_id, "society_id": current_active_admin["society_id"]})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Form not found")
    return {"detail": "Form deleted"}

# Get all responses of a user's form
@admin_router.get("/forms/{form_id}/responses", response_model=List[FormSubmission])
async def get_form_responses(form_id: str, current_admin: Annotated[Admin, Depends(get_current_admin)]):
    current_active_admin = admin_serial(current_admin)
    submissions = form_submissions_collection.find({"form_id": form_id, "society_id": current_active_admin["society_id"]})
    return [FormSubmission(**submission) for submission in submissions]


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