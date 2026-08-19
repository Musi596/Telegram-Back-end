from sqlalchemy.orm import Session
import secrets
from bots.models import Bot


def get_bot(db: Session, bot_id: int):
    return db.query(Bot).filter(Bot.id == bot_id).first()


def get_user_bots(db: Session, user_id: int):
    return db.query(Bot).filter(Bot.user_id == user_id).all()


def get_bot_by_token(db: Session, token: str):
    return db.query(Bot).filter(Bot.token == token).first()


def create_bot(db: Session, user_id: int, name: str, username: str, description: str = None):
    token = secrets.token_urlsafe(32)
    db_bot = Bot(
        user_id=user_id,
        name=name,
        username=username,
        token=token,
        description=description
    )
    db.add(db_bot)
    db.commit()
    db.refresh(db_bot)
    return db_bot


def delete_bot(db: Session, bot_id: int):
    db_bot = get_bot(db, bot_id)
    if db_bot:
        db.delete(db_bot)
        db.commit()