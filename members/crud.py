from sqlalchemy.orm import Session
from members.models import Member


def get_member(db: Session, chat_id: int, user_id: int):
    return db.query(Member).filter(
        Member.chat_id == chat_id,
        Member.user_id == user_id
    ).first()


def get_chat_members(db: Session, chat_id: int):
    return db.query(Member).filter(Member.chat_id == chat_id).all()


def get_members_count(db: Session, chat_id: int):
    return db.query(Member).filter(Member.chat_id == chat_id).count()


def is_member(db: Session, chat_id: int, user_id: int):
    return get_member(db, chat_id, user_id) is not None


def is_admin(db: Session, chat_id: int, user_id: int):
    member = get_member(db, chat_id, user_id)
    return member and member.role in ["owner", "admin"]


def add_member(db: Session, chat_id: int, user_id: int, role: str = "member"):
    existing = get_member(db, chat_id, user_id)
    if existing:
        return existing
    db_member = Member(chat_id=chat_id, user_id=user_id, role=role)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


def remove_member(db: Session, chat_id: int, user_id: int):
    db_member = get_member(db, chat_id, user_id)
    if db_member:
        db.delete(db_member)
        db.commit()


def update_member(db: Session, chat_id: int, user_id: int, data):
    db_member = get_member(db, chat_id, user_id)
    for key, value in data.model_dump(exclude_none=True).items():
        setattr(db_member, key, value)
    db.commit()
    db.refresh(db_member)
    return db_member