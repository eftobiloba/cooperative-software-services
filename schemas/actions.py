from models.forms import Action

def action_serial(action: Action) -> dict:
    return {
        "action_name": action.action_name,
        "action_id": action.action_id,
        "action_icon": action.action_icon,
        "is_public": action.is_public,
        "action_description": action.action_description,
        "version": action.version,
        "status": action.status,
        "action_type": action.action_type,
        "subactions": [subaction.dict() for subaction in action.subactions],
        "developer_id": action.developer_id,
        "society_id": action.society_id if action.society_id else [],
    }

def list_actions_serial(actions) -> list:
    return [action_serial(action) for action in actions]
    