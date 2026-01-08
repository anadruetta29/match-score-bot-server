from app.database.session import SessionLocal
from app.database.models.session import SessionModel
from app.config.exceptions.session_not_found import SessionNotFoundError
from datetime import datetime, UTC


class SessionRepository:

    def create(self, session_id: str):
        db = SessionLocal()
        try:
            session = SessionModel(id=session_id)
            db.add(session)
            db.commit()
        finally:
            db.close()

    def finish(self, session_id: str, final_score: int):
        db = SessionLocal()
        try:
            session = db.query(SessionModel).filter_by(id=session_id).first()
            if not session:
                raise SessionNotFoundError(session_id)

            session.finished_at = datetime.now(UTC)
            session.final_score = final_score
            db.commit()
        finally:
            db.close()

