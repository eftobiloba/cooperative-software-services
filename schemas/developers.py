from models.devs import Developer

def developer_serial(dev: Developer) -> dict:
    return{
        "dev_name": dev["dev_name"],
        "dev_id": dev["dev_id"],
        "dev_description": dev["dev_description"],
        "dev_email": dev["dev_email"],
        "dev_access_token": dev["dev_access_token"],
        "status": dev["status"],
        "actions": dev["actions"] if dev["actions"] else [],
        "forms": dev["forms"] if dev["forms"] else [],
        "password": dev["password"]
    }

def list_developer_serial(devs) -> list:
    return [developer_serial(dev) for dev in devs]