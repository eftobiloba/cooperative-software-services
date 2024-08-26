from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ExecuteSubActionRequest(BaseModel):
    action_id: str
    subaction_id: str
    form_data: Optional[Dict[str, Any]] = None
    additional_input: Optional[Dict[str, Any]] = None
    from_submit: bool = False

class Params(BaseModel):
    param_id: str
    data: str

class ActionField(BaseModel):
    field_id: str
    field_value: Optional[str] = None  # Default to None until filled
    field_type: str  # e.g., 'text', 'number', 'email', etc.

class SubAction(BaseModel):
    subaction_name: str
    subaction_id: str
    action_id: str
    endpoint: str
    fields: Optional[List[ActionField]]  # Fields required for this subaction
    requires_input: bool  # Whether the subaction requires user input

class FieldMapping(BaseModel):
    form_field: str
    action_field: str

class Action(BaseModel):
    action_name: str
    action_id: str
    action_icon: str
    action_description: str
    is_public: bool
    version: str
    status: str
    action_type: str  # 'trigger_based', 'submission_based', 'choice_based'
    subactions: List[SubAction]
    developer_id: str
    society_id: Optional[List[str]]

class Field(BaseModel):
    field_name: str
    field_type: str
    field_id: str
    required: bool = False
    options: Optional[List[str]] = []
    onCompletelyFilled: Optional[Action] = None
    promptMessage: Optional[str] = ''

class Executable(BaseModel):
    action_id: str
    subaction_id: str

class Form(BaseModel):
    title: str
    developer_id: Optional[str]
    society_id: Optional[str] = None
    product_id: Optional[str] = None
    is_public: str
    is_visible: str
    form_id: str
    description: str
    fields: List[Field]
    onSubmit: Optional[Executable]
    onApprove: Optional[Executable] = None
    onDecline: Optional[Executable] = None

class FormInDB(Form):
    id: str

class FormSubmission(BaseModel):
    form_id: str
    data: dict

def form_serial(form: Form) -> dict:
    return {
        "fields": form["fields"],
        "submit_actions": form["onSubmit"] if form["onSubmit"] else {},
        "approve_actions": form["onApprove"] if form["onApprove"] else {},
        "decline_actions": form["onDecline"] if form["onDecline"] else {},
    }

def form_helper(form) -> FormInDB:
    serial = form_serial(form)
    
    return FormInDB(
        id=str(form["_id"]),
        form_id=str(form["form_id"]),
        society_id=form["society_id"],
        product_id=form["product_id"],
        developer_id=form["developer_id"],
        is_public=form["is_public"],
        is_visible=form["is_visible"],
        title=form["title"],
        description=form["description"],
        fields=serial.get("fields"),
        onSubmit=serial.get("submit_actions") if serial.get("submit_actions") else None,
        onApprove=serial.get("approve_actions") if serial.get("approve_actions") else None,
        onDecline=serial.get("decline_actions")if serial.get("decline_actions") else None,
    )