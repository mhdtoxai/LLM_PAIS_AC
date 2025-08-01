import re
import json
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from manager import ai_manager
from db.crud.crud import get_user, create_user, update_user
from db.models.models import User
from chat.extract_history import extract_history

chat_router= APIRouter()

class Message(BaseModel):
    from_: str = Field(..., alias='from')
    query: str
    member: bool = False
    organization_id: str

@chat_router.post("/")
async def chat_api(request: Request):
    try:
        data = await request.json()
        message = Message(**data)
        print("Message: ", message)

        user = await get_user(message.from_, message.organization_id)

        if user is None:
            user = await create_user(User(
                msisdn=message.from_,
                organization_id=message.organization_id,
                chat_history='CHAT HISTORY: ',
                status=1
            ))
            user_chat_history = user["chat_history"]
        else:
            user_chat_history = user["chat_history"]

        user_chat_history += "USER: " + str(message.query) + ", "

        extract = await extract_history(user_chat_history)
        chat_history = extract['chat_history']
        chat_history += "USER: " + str(message.query) + ", "

        if extract['error'] is not None:
            chat_history = message.query

        response_message = ai_manager(chat_history, member=message.member)
        response_message = response_message.replace('**', '*')
        user_chat_history += "ASSISTANT: " + response_message + ", "

        await update_user(user["_id"], user_chat_history)

        if message.member:
            response_message = response_message.replace('\n', '').replace('\\"', '"')

        json_match = re.search(r'\{.*\}', response_message)
        print("JSON Match: ", json_match)

        if json_match:
            try:
                json_data = json.loads(json_match.group())
                print("JSON extraído:", json_data)
                return {
                    "from": message.from_,
                    "message": json_data.get("mensaje", "No se encontró el mensaje"),
                    "action": json_data.get("action", "No se encontró la acción"),
                }
            except json.JSONDecodeError:
                print("El JSON extraído no es válido.")

        return {
            "from": message.from_,
            "response": response_message
        }

    except Exception as e:
        return {
            "error": str(e),
            "message": "Error in the request",
            "status": 500
        }
