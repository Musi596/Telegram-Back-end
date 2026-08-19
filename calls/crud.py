from sqlalchemy.orm import Session
from datetime import datetime
from calls.models import Call


def get_call(db: Session, call_id: int):
    return db.query(Call).filter(Call.id == call_id).first()


def get_user_calls(db: Session, user_id: int, skip: int = 0, limit: int = 20):
    return db.query(Call).filter(
        (Call.caller_id == user_id) | (Call.receiver_id == user_id)
    ).order_by(Call.created_at.desc()).offset(skip).limit(limit).all()


def create_call(db: Session, caller_id: int, receiver_id: int, type: str):
    db_call = Call(
        caller_id=caller_id,
        receiver_id=receiver_id,
        type=type,
        status="pending",
        started_at=datetime.utcnow()
    )
    db.add(db_call)
    db.commit()
    db.refresh(db_call)
    return db_call


def end_call(db: Session, call_id: int, status: str):
    db_call = get_call(db, call_id)
    if db_call:
        db_call.status = status
        db_call.ended_at = datetime.utcnow()
        db.commit()
        db.refresh(db_call)
    return db_call