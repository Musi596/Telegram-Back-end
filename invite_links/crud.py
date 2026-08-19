from sqlalchemy.orm import Session
from invite_links.models import InviteLink
import secrets


def get_invite_link(db: Session, link: str):
    return db.query(InviteLink).filter(InviteLink.link == link).first()


def get_chat_invite_links(db: Session, chat_id: int):
    return db.query(InviteLink).filter(
        InviteLink.chat_id == chat_id,
        InviteLink.is_active == True
    ).all()


def create_invite_link(db: Session, chat_id: int, user_id: int, expires_at=None):
    link = secrets.token_urlsafe(16)
    db_link = InviteLink(
        chat_id=chat_id,
        created_by=user_id,
        link=link,
        expires_at=expires_at
    )
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link


def revoke_invite_link(db: Session, link_id: int):
    db_link = db.query(InviteLink).filter(InviteLink.id == link_id).first()
    if db_link:
        db_link.is_active = False
        db.commit()
        db.refresh(db_link)
    return db_link