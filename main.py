
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from chat.chat import chat_router
from auth.auth import verify_token

app = FastAPI( docs_url='/docs')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/pais", dependencies=[Depends(verify_token)])
