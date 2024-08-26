from fastapi import APIRouter
from pydantic import BaseModel
from tests.test_actions import data_backup_action
from models.forms import ExecuteSubActionRequest
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
from modules.action.engine import execute_subaction_trigger

action_router = APIRouter()

# Dummy function for getting the action

@action_router.post("/execute_subaction/")
async def execute_subaction(request: ExecuteSubActionRequest):
    response = await execute_subaction_trigger(request)
    return response