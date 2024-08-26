from fastapi import APIRouter
from models.admins import Admin
from models.societies import Society
from modules.security import passwordSSH
from config.database import admin_collection, society_collection, dev_collection
from schemas.developers import list_developer_serial
from schemas.societies import *
from models.devs import Developer
from modules.security.accessTokenGen import generate_access_token

def society_exists(society_id):
    society = society_collection.find_one({"society_id": society_id})
    if society:
        return True
    else:
        return False

master_router = APIRouter()

@master_router.get("/admins/")
async def get_admins():
    admins = list_admin_serial(admin_collection.find())
    return admins

@master_router.get("/societies/")
async def get_societies():
    societies = list_society_serial(society_collection.find())
    return societies

@master_router.get("/devs/")
async def get_devs():
    developers = list_developer_serial(dev_collection.find())
    return developers

@master_router.get("/societies/one/{society_id}")
async def get_one_society(society_id: str):
    society = society_serial(society_collection.find_one({"society_id": society_id}))
    if society:
        return {"code": "00", "message": "success", "data": society}
    else:
        return {"code": "01", "message": "failure", "data": "Society not found"}

@master_router.post('/admins/new')
async def create_admin(request:Admin):
    admin_object = dict(request)
    if society_exists(admin_object["society_id"]):
        hashed_pass = passwordSSH.hash_password(request.password)
        admin_object["password"] = hashed_pass
        username = admin_object["admin_id"] +'_'+ admin_object["society_id"]
        admin_object["username"] = username
        admin_collection.insert_one(admin_object)
        return {"code": "00", "message": "success", "data": "Admin added successfully"}
    else:
        return {"code": "01", "message": "failure", "data": "Society not found"}

@master_router.post('/societies/new')
async def create_new_society(request:Society):
    society_object = dict(request)
    society_collection.insert_one(society_object)
    return {"code": "00", "message": "success", "data": "Society created successfully"}

@master_router.post('/developers/new')
async def create_developer(request: Developer):
    hashed_pass = passwordSSH.hash_password(request.password)
    dev_object = dict(request)
    dev_object["password"] = hashed_pass
    access_token = generate_access_token()
    dev_object["dev_access_token"] = access_token
    dev_collection.insert_one(dev_object)
    return {"code": "00", "message": "success", "data": "Developer created successfully"}

@master_router.put('/developers/approve/{dev_id}')
async def approve_developer(dev_id: str):
    request = dev_collection.find_one({"dev_id": dev_id})
    dev_object = dict(request)
    dev_object["status"] = "approved"
    access_token = generate_access_token()
    dev_object["dev_access_token"] = access_token
    updated_dev = dev_collection.find_one_and_update({"dev_id": dev_id}, {"$set":dev_object})

    if updated_dev:
        return {"code": "00", "message": "success", "data": "Developer approved"}
    else:
        return {"code": "01", "message": "failure", "data": "Developer not found"}