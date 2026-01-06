from app.domain.entities.session import Session

class ChatSessionState:
    def __init__(self, session: Session, questions: list):
        self.session = session
        self.selected_questions = questions
        self.step = 0
