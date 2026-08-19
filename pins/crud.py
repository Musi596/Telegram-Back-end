from sqlalchemy.orm import Session
from pins.models import Pin


def get_pin(db: Session, chat_id: int, message_id: int):
    return db.query(Pin).filter(
        Pin.chat_id == chat_id,
        Pin.message_id == message_id
    ).first()


def get_chat_pins(db: Session, chat_id: int):
    return db.query(Pin).filter(Pin.chat_id == chat_id).all()


def get_last_pin(db: Session, chat_id: int):
    return db.query(Pin).filter(
        Pin.chat_id == chat_id
    ).order_by(Pin.pinned_at.desc()).first()


def pin_message(db: Session, chat_id: int, message_id: int, user_id: int):
    existing = get_pin(db, chat_id, message_id)
    if existing:
        return existing
    db_pin = Pin(chat_id=chat_id, message_id=message_id, pinned_by=user_id)
    db.add(db_pin)
    db.commit()
    db.refresh(db_pin)
    return db_pin


def unpin_message(db: Session, chat_id: int, message_id: int):
    db_pin = get_pin(db, chat_id, message_id)
    if db_pin:
        db.delete(db_pin)
        db.commit()