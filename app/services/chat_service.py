from app.services.session_service import SessionService
from app.services.score_service import ScoreService
from app.services.question_service import QuestionService

score_service = ScoreService()


class ChatService:

    def handle_message(self, option_id: int | None, session_id: str | None):
        session_id, session = SessionService.get_or_create(session_id)

        questions = QuestionService.load()
        step = session["step"]

        if option_id is not None and step > 0:
            prev_question = questions[step - 1]
            selected_option = prev_question["options"][option_id]

            session["answers"].append(
                {
                    "question_id": prev_question["id"],
                    "option_id": option_id,
                    "score": selected_option["score"],
                }
            )

        if step < len(questions):
            question = questions[step]
            session["step"] += 1

            return session_id, question, None, False

        score = score_service.calculate(session["answers"])

        return session_id, f"Your match score is {score}/10", score, True
