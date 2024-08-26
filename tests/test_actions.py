from models.forms import Action, SubAction
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests

data_backup_action = Action(
    action_name="Data Backup Trigger",
    action_id="data-backup-trigger",
    action_icon="data_backup.png",
    action_description="Triggers a backup of a membership form on submit.",
    is_public=True,
    action_type='trigger_based',
    version="1.0",
    status="active",
    subactions=[
        SubAction(
            subaction_name="Backup Data",
            subaction_id="data_backup",
            action_id="data-backup-trigger",
            endpoint="http://localhost:8000/test/data_backup",
            fields=[],
            requires_input=False
        )
    ],
    developer_id="techify-labs",
    society_id=[]
)

router = APIRouter()

# Request model for processing payment
class WithdrawalInfo(BaseModel):
    name: str
    membership_no: str
    amount: float
    account_no: str
    bank_name: str

@router.get("/data_backup")
async def welcome_view():
    return {"message": "Welcome to quick data backup!"}

@router.post("/data_backup")
async def backup_data(request: WithdrawalInfo):
    payload = dict(request)
    # Call external payment gateway API
    try:
        response = requests.post("http://demo0565819.mockable.io/user", json=payload)
        if response.status_code == 200:
            # Corrected the response.json() usage
            response_data = response.json()

            # Writing the response data to a file
            with open("demofile2.txt", "w") as f:
                f.write(str(payload))  # Convert the dictionary to a string before writing

            return {"code": "00", "message": "Form submitted, Data backed up successfully"}
        else:
            raise HTTPException(status_code=400, detail="Backup failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Register the router with the main application
# app.include_router(router)
