from pydantic import BaseModel
from typing import List

class Field(BaseModel):
    name: str
    type: str  # "text", "number", "options"
    options: List[str] = None  # Only used if type is "options"

class Params(BaseModel):
    param_id: str
    data: str

class Action(BaseModel):
    name: str
    params: List[Params]
    url: str

class Form(BaseModel):
    title: str
    society_id: str
    product_id: str
    description: str
    fields: List[Field]
    onSubmit: List[Action]
    onApprove: List[Action]
    onDecline: List[Action]

class FormInDB(Form):
    id: str

class FormSubmission(BaseModel):
    form_id: str
    data: dict

def form_helper(form) -> FormInDB:
    fields = [Field(**field) for field in form["fields"]]
    submit_actions = [Action(**onSubmit) for onSubmit in form["onSubmit"]]
    approve_actions = [Action(**onApprove) for onApprove in form["onApprove"]]
    decline_actions = [Action(**onDecline) for onDecline in form["onDecline"]]
    return FormInDB(
        id=str(form["_id"]),
        product_id=str(form["product_id"]),
        society_id=form["society_id"],
        title=form["title"],
        description=form["description"],
        fields=fields,
        onSubmit=submit_actions,
        onApprove=approve_actions,
        onDecline=decline_actions,
    )
