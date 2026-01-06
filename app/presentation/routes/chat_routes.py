from fastapi import APIRouter
from app.presentation.controllers.chat_controller import chat

router = APIRouter(prefix="/chat", tags=["Chat"])

router.post("/")(chat)
