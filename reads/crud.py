from sqlalchemy.orm import Session
from reads.models import Read


def read_message(db: Session, message_id: int, user_id: int):
    existing = db.query(Read).filter(
        Read.message_id == message_id,
        Read.user_id == user_id
    ).first()
    if existing:
        return existing
    db_read = Read(message_id=message_id, user_id=user_id)
    db.add(db_read)
    db.commit()
    db.refresh(db_read)
    return db_read


def get_unread_count(db: Session, chat_id: int, user_id: int):
    from messages.models import Message
    messages = db.query(Message).filter(
        Message.chat_id == chat_id,
        Message.user_id != user_id,
        Message.is_deleted == False
    ).all()
    message_ids = [m.id for m in messages]
    read_ids = [r.message_id for r in db.query(Read).filter(
        Read.message_id.in_(message_ids),
        Read.user_id == user_id
    ).all()]
    return len(set(message_ids) - set(read_ids))


def mark_all_read(db: Session, chat_id: int, user_id: int):
    from messages.models import Message
    messages = db.query(Message).filter(
        Message.chat_id == chat_id,
        Message.user_id != user_id,
        Message.is_deleted == False
    ).all()
    for message in messages:
        existing = db.query(Read).filter(
            Read.message_id == message.id,
            Read.user_id == user_id
        ).first()
        if not existing:
            db.add(Read(message_id=message.id, user_id=user_id))
    db.commit()