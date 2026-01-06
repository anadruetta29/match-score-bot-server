from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.services.session_service import SessionService
from app.domain.models.answer import Answer
from utils.load_questions import load_questions
app = FastAPI(title="Match Score Bot API")

questions_dataset = load_questions()

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    session = None
    step = 0

    try:
        while True:
            data = await websocket.receive_json()
            option_id = data.get("option_id")
            session_id = data.get("session_id")

            if not session:
                session = SessionService.get_or_create(session_id)

            if step > 0:
                current_question = questions_dataset[step - 1]
                answer = Answer(
                    question_id=current_question["id"],
                    option_id=option_id,
                    score=current_question["options"][option_id]["score"]
                )
                session.add_answer(answer)

            finished = step >= len(questions_dataset)

            next_question = None
            if not finished:
                next_question = questions_dataset[step]
                step += 1

            chat_response = {
                "session_id": session.session_id,
                "question": next_question,
                "result": {"score": session.get_score().total_score} if finished else None,
                "finished": finished
            }

            await websocket.send_json(chat_response)

            if finished:
                break

    except WebSocketDisconnect:
        print(f"Cliente desconectado: {session.session_id if session else 'desconocido'}")
