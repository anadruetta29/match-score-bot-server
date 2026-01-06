from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.services.session_service import SessionService
from app.domain.models.answer import Answer
from app.utils.load_questions import load_questions
import random

app = FastAPI(title="Match Score Bot API")
questions_dataset = load_questions()

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    session = None
    step = 0
    started = False

    num_questions = min(10, len(questions_dataset))
    selected_questions = random.sample(questions_dataset, k=num_questions)

    try:
        welcome_message = {
            "session_id": None,
            "question": {
                "id": "welcome",
                "text": "¡Hola! Gracias por venir a buscar consejo en mí, ¿Estás listo para saber si es un buen match?",
                "options": [
                    {"id": 0, "label": "Sí"},
                    {"id": 1, "label": "No"}
                ]
            },
            "result": None,
            "finished": False
        }
        await websocket.send_json(welcome_message)

        while True:
            data = await websocket.receive_json()
            option_id = data.get("option_id")
            session_id = data.get("session_id")

            if not started:
                if option_id == 0:  # Sí
                    session = SessionService.get_or_create(session_id)
                    started = True
                    step = 0
                else:
                    chat_response = {
                        "session_id": session_id,
                        "question": None,
                        "result": {"score": 0},
                        "finished": True
                    }
                    await websocket.send_json(chat_response)
                    await websocket.close()
                    break

            if step > 0:
                current_question = selected_questions[step - 1]
                answer = Answer(
                    question_id=current_question["id"],
                    option_id=option_id,
                    score=current_question["options"][option_id]["score"]
                )
                session.add_answer(answer)

            finished = step >= len(selected_questions)

            next_question = None
            if not finished:
                next_question = selected_questions[step]
                step += 1

            chat_response = {
                "session_id": session.session_id,
                "question": next_question,
                "result": {"score": session.get_score().total_score} if finished else None,
                "finished": finished
            }

            await websocket.send_json(chat_response)

            if finished:
                await websocket.close()
                break

    except WebSocketDisconnect:
        print(f"Cliente desconectado: {session.session_id if session else 'desconocido'}")
