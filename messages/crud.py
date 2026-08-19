from sqlalchemy.orm import Session
from messages.models import Message


def get_message(db: Session, message_id: int):
    return db.query(Message).filter(Message.id == message_id).first()


def get_chat_messages(db: Session, chat_id: int, skip: int = 0, limit: int = 50):
    return db.query(Message).filter(
        Message.chat_id == chat_id,
        Message.is_deleted == False
    ).order_by(Message.created_at.desc()).offset(skip).limit(limit).all()


def get_last_message(db: Session, chat_id: int):
    return db.query(Message).filter(
        Message.chat_id == chat_id,
        Message.is_deleted == False
    ).order_by(Message.created_at.desc()).first()


def create_message(db: Session, chat_id: int, user_id: int, text: str = None, media_id: int = None, reply_to_id: int = None):
    db_message = Message(
        chat_id=chat_id,
        user_id=user_id,
        text=text,
        media_id=media_id,
        reply_to_id=reply_to_id
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def update_message(db: Session, message_id: int, text: str):
    from datetime import datetime
    db_message = get_message(db, message_id)
    db_message.text = text
    db_message.is_edited = True
    db_message.edited_at = datetime.utcnow()
    db.commit()
    db.refresh(db_message)
    return db_message


def delete_message(db: Session, message_id: int):
    db_message = get_message(db, message_id)
    db_message.is_deleted = True
    db.commit()


def forward_message(db: Session, message_id: int, to_chat_id: int, user_id: int):
    original = get_message(db, message_id)
    db_message = Message(
        chat_id=to_chat_id,
        user_id=user_id,
        text=original.text,
        media_id=original.media_id,
        forward_from_id=message_id
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message