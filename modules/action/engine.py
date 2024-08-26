from fastapi import HTTPException
from typing import Dict, Any, Optional
import httpx
from models.forms import SubAction, Action, ExecuteSubActionRequest
from tests.test_actions import data_backup_action
from pydantic import BaseModel

def get_action(action_id: str) -> Action:
    action = data_backup_action
    return action

async def execute_subaction_trigger(request: ExecuteSubActionRequest):
    # Retrieve the action and subaction
    action = get_action(request.action_id)
    subaction = next((sa for sa in (action.subactions or []) if sa.subaction_id == request.subaction_id), None)

    if not subaction:
        raise HTTPException(status_code=404, detail="Subaction not found")

    # Initialize additional_input
    additional_input = request.additional_input

    # Handle choice-based actions requiring additional input
    if action.action_type == "choice_based" and subaction.requires_input and not additional_input:
        if request.form_data:
            raise HTTPException(status_code=400, detail="Additional input required for choice-based actions")
        else:
            # Trigger the form to get additional input (e.g., show a popup)
            form_response = await get_additional_input_from_user(subaction)
            if form_response.get("requires_input"):
                return form_response  # Return the required fields to the frontend for dynamic form rendering

            additional_input = form_response.get("user_input")
            if not additional_input:
                raise HTTPException(status_code=400, detail="User did not provide required input")

    # Execute the appropriate subaction based on the action type
    if action.action_type == "trigger_based":
        return await execute_trigger_based_action(subaction, request.form_data, additional_input)
    elif action.action_type == "submission_based":
        return await execute_submission_based_action(subaction, request.form_data, additional_input)
    elif action.action_type == "choice_based":
        return await execute_choice_based_action(subaction, additional_input)
    else:
        raise HTTPException(status_code=400, detail="Invalid action type")

async def execute_trigger_based_action(subaction: SubAction, form_data: Optional[Dict[str, Any]], additional_input: Optional[Dict[str, Any]]):
    if not form_data:
        raise HTTPException(status_code=400, detail="Form data required for trigger-based actions")

    data = map_fields(form_data, additional_input)
    response = await trigger_subaction(subaction, data)
    if not response.get("success", True):  # Assuming "success" is the key in the response that indicates failure
        raise HTTPException(status_code=500, detail=f"{subaction.subaction_name} failed")
    
    return response  # Return the response from the subaction endpoint

async def execute_submission_based_action(subaction: SubAction, form_data: Optional[Dict[str, Any]], additional_input: Optional[Dict[str, Any]]):
    if not form_data:
        raise HTTPException(status_code=400, detail="Form data required for trigger-based actions")

    data = map_fields(form_data, additional_input)
    response = await trigger_subaction(subaction, data)
    if not response.get("success", True):  # Assuming "success" is the key in the response that indicates failure
        raise HTTPException(status_code=500, detail=f"{subaction.subaction_name} failed")
    
    return response  # Return the response from the subaction endpoint

async def execute_choice_based_action(subaction: SubAction, additional_input: Optional[Dict[str, Any]]):
    if subaction.requires_input and not additional_input:
        raise HTTPException(status_code=400, detail="Additional input required for choice-based actions")

    response = await trigger_subaction(subaction, additional_input)
    if not response.get("success", True):  # Assuming "success" is the key in the response that indicates failure
        raise HTTPException(status_code=500, detail=f"{subaction.subaction_name} failed")

    return response

def map_fields(form_data: Optional[Dict[str, Any]], additional_input: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    form_data = form_data or {}
    additional_input = additional_input or {}
    return {**form_data, **additional_input}

async def trigger_subaction(subaction: SubAction, data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(subaction.endpoint, json=data)
        if response.status_code == 200:
            return response.json()  # Return the exact response from the subaction endpoint
        else:
            return {"success": False, "message": f"Subaction {subaction.subaction_name} failed with status {response.status_code}"}
    except Exception as e:
        return {"success": False, "message": str(e)}

async def get_additional_input_from_user(subaction: SubAction):
    if subaction.requires_input:
        if not subaction.fields:
            raise HTTPException(status_code=400, detail="Required fields are not defined for this subaction")
        return {
            "requires_input": True,
            "required_fields": subaction.fields  # Send this to the frontend
        }
    return None