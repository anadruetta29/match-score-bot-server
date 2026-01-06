from app.domain.dto.chat.request.chat_req import ChatRequest
from app.domain.dto.chat.response.chat_res import ChatResponse
from app.services.chat_service import ChatService

service = ChatService()

def chat(request: ChatRequest) -> ChatResponse:
    session_id, reply, score, finished = service.handle_message(
        request.message,
        request.session_id
    )

    return ChatResponse(
        reply=reply,
        session_id=session_id,
        score=score,
        finished=finished
    )
