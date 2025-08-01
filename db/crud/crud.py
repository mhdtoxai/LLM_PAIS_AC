from db.models.models import User
from db.db import get_collection
import os

if not os.getenv('MONGODB_COLLECTION'):
    raise ValueError("MONGODB_COLLECTION no encontrada, revisar .env")

collection = get_collection(os.getenv('MONGODB_COLLECTION')) 

async def get_user(msisdn, organization_id):
    user_data = collection.find_one({"msisdn": msisdn, "organization_id": organization_id})
    if user_data is None:
        return None
    return user_data

async def create_user(user):
    insert_result = collection.insert_one(user.dict(by_alias=True))
    if insert_result is None:
        return None
    user_data = collection.find_one({
        "msisdn": user.msisdn,
        "organization_id": user.organization_id
    })
    return user_data

async def update_user(user_id: str, chat_history: str):
    return collection.update_one({"_id": user_id}, {"$set": {"chat_history": chat_history}})
