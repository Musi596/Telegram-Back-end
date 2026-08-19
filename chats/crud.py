from sqlalchemy.orm import Session
from chats.models import Chat


def get_chat(db: Session, chat_id: int):
    return db.query(Chat).filter(Chat.id == chat_id).first()


def get_chat_by_username(db: Session, username: str):
    return db.query(Chat).filter(Chat.username == username).first()


def get_user_chats(db: Session, user_id: int):
    from members.models import Member
    member_chat_ids = [m.chat_id for m in db.query(Member).filter(Member.user_id == user_id).all()]
    return db.query(Chat).filter(Chat.id.in_(member_chat_ids)).all()


def create_chat(db: Session, owner_id: int, type: str, name: str = None, description: str = None, photo: str = None, is_public: bool = False, username: str = None):
    db_chat = Chat(
        owner_id=owner_id,
        type=type,
        name=name,
        description=description,
        photo=photo,
        is_public=is_public,
        username=username
    )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat


def update_chat(db: Session, chat_id: int, data):
    db_chat = get_chat(db, chat_id)
    for key, value in data.model_dump(exclude_none=True).items():
        setattr(db_chat, key, value)
    db.commit()
    db.refresh(db_chat)
    return db_chat


def delete_chat(db: Session, chat_id: int):
    db_chat = get_chat(db, chat_id)
    db.delete(db_chat)
    db.commit()