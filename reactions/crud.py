from sqlalchemy.orm import Session
from reactions.models import Reaction


def get_reaction(db: Session, message_id: int, user_id: int, emoji: str):
    return db.query(Reaction).filter(
        Reaction.message_id == message_id,
        Reaction.user_id == user_id,
        Reaction.emoji == emoji
    ).first()


def get_message_reactions(db: Session, message_id: int):
    return db.query(Reaction).filter(Reaction.message_id == message_id).all()


def add_reaction(db: Session, message_id: int, user_id: int, emoji: str):
    existing = get_reaction(db, message_id, user_id, emoji)
    if existing:
        return existing
    db_reaction = Reaction(message_id=message_id, user_id=user_id, emoji=emoji)
    db.add(db_reaction)
    db.commit()
    db.refresh(db_reaction)
    return db_reaction


def remove_reaction(db: Session, message_id: int, user_id: int, emoji: str):
    db_reaction = get_reaction(db, message_id, user_id, emoji)
    if db_reaction:
        db.delete(db_reaction)
        db.commit()