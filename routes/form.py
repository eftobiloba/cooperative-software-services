from fastapi import APIRouter, HTTPException
from bson import ObjectId
from typing import List
from models.forms import FormInDB, Form, form_helper, FormSubmission
from config.database import forms_collection, form_submissions_collection

form_router = APIRouter()

# Create a new form
@form_router.post("/forms/", response_model=FormInDB)
async def create_form(form: Form):
    form_dict = form.dict()
    result = forms_collection.insert_one(form_dict)
    new_form = forms_collection.find_one({"_id": result.inserted_id})
    return form_helper(new_form)

# Get a form by ID
@form_router.get("/forms/{form_id}", response_model=FormInDB)
async def get_form(form_id: str):
    form = forms_collection.find_one({"_id": ObjectId(form_id)})
    if form is None:
        raise HTTPException(status_code=404, detail="Form not found")
    return form_helper(form)

# Get all forms
@form_router.get("/forms/", response_model=List[FormInDB])
async def get_all_forms():
    forms = forms_collection.find()
    return [form_helper(form) for form in forms]

# Update a form by ID
@form_router.put("/forms/{form_id}", response_model=FormInDB)
async def update_form(form_id: str, updated_form: Form):
    result = forms_collection.update_one({"_id": ObjectId(form_id)}, {"$set": updated_form.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Form not found")
    updated_form = forms_collection.find_one({"_id": ObjectId(form_id)})
    return form_helper(updated_form)

# Delete a form by ID
@form_router.delete("/forms/{form_id}")
async def delete_form(form_id: str):
    result = forms_collection.delete_one({"_id": ObjectId(form_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Form not found")
    return {"detail": "Form deleted"}

# Submit to a form created by a user
@form_router.post("/forms/{form_id}/submit", response_model=FormSubmission)
async def submit_form(form_id: str, submission: FormSubmission):
    submission_dict = submission.dict()
    submission_dict["form_id"] = form_id
    result = form_submissions_collection.insert_one(submission_dict)
    new_submission = form_submissions_collection.find_one({"_id": result.inserted_id})
    return FormSubmission(**new_submission)

# Get all responses of a user's form
@form_router.get("/forms/{form_id}/responses", response_model=List[FormSubmission])
async def get_form_responses(form_id: str):
    submissions = form_submissions_collection.find({"form_id": form_id})
    return [FormSubmission(**submission) for submission in submissions]
