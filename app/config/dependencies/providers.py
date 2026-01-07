from app.services.application.chat_service import ChatService
from app.services.application.chat_session_state import ChatSessionStateService
from app.services.interfaces.chat_interface import ChatServiceInterface
from app.services.interfaces.chat_session_state_interface import ChatSessionStateServiceInterface

def get_chat_service() -> ChatServiceInterface:
    return ChatService()


def get_chat_session_state_service() -> ChatSessionStateServiceInterface:
    return ChatSessionStateService()
