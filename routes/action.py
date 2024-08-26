from fastapi import APIRouter
from pydantic import BaseModel
from tests.test_actions import data_backup_action
from models.forms import ExecuteSubActionRequest, Action
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
from modules.action.engine import execute_subaction_trigger
from config.database import actions_collection

action_router = APIRouter()

# Dummy function for getting the action

@action_router.post("/execute_subaction/")
async def execute_subaction(request: ExecuteSubActionRequest):
    response = await execute_subaction_trigger(request)
    return response

@action_router.post("/save", response_model=Action)
async def create_action(action: Action):
    try:
        # Serialize the action according to your existing process
        serialized_action = action.dict()
        
        # Insert into the database
        result = actions_collection.insert_one(serialized_action)
        
        # Fetch the inserted action to return it
        created_action = actions_collection.find_one({"_id": result.inserted_id})
        
        return created_action
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))