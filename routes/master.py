from fastapi import APIRouter
from models.admins import Admin
from modules.security import passwordSSH
from config.database import admin_collection
from schemas.societies import *

master_router = APIRouter()

@master_router.get("/")
async def get_admins():
    admins = list_admin_serial(admin_collection.find())
    return admins

@master_router.post('/new/admin')
async def create_admin(request:Admin):
    hashed_pass = passwordSSH.hash_password(request.password)
    admin_object = dict(request)
    admin_object["password"] = hashed_pass
    admin_collection.insert_one(admin_object)
    return {"code": "00", "message": "success", "data": "Admin added successfully"}