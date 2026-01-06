from app.services.session_service import SessionService
from app.services.score_service import ScoreService
from app.services.question_service import QuestionService
from app.domain.entities.answer import Answer
from app.domain.entities.session import Session
from app.database.repository.session import SessionRepository
from app.database.repository.answer import AnswerRepository
from app.services.chat_session_state import ChatSessionState
import random

score_service = ScoreService()
session_service = SessionService()
question_service = QuestionService()

answer_repository = AnswerRepository()
session_repository = SessionRepository()

class ChatService:
    def __init__(self):
        self.num_questions_per_session = 10

    def start_session(self, session_id: str | None):
        session = session_service.get_or_create(session_id)
        session_repository.create(session.session_id)

        questions = question_service.load()
        selected = random.sample(
            questions,
            k=min(self.num_questions_per_session, len(questions))
        )

        return ChatSessionState(session, selected)

    def handle_answer(self, state: ChatSessionState, option_id: int | None):

        if state.step > 0 and option_id is not None:
            prev_question = state.selected_questions[state.step - 1]
            score = prev_question["options"][option_id]["score"]

            answer = Answer(
                question_id=prev_question["id"],
                option_id=option_id,
                score=score
            )

            state.session.add_answer(answer)
            answer_repository.save(state.session.session_id, answer)

        finished = state.step >= len(state.selected_questions)

        next_question = None
        if not finished:
            next_question = state.selected_questions[state.step]
            state.step += 1

        result = None
        if finished:
            raw_score = state.session.get_score().total_score
            max_score_total = sum(
                max(opt["score"] for opt in q["options"])
                for q in state.selected_questions
            )

            normalized = score_service._normalize(raw_score, max_score_total)
            session_repository.finish(state.session.session_id, raw_score)
            result = {"score": normalized}

        return next_question, result, finished

