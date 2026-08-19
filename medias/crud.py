from sqlalchemy.orm import Session
from medias.models import Media
from medias.schemas import MediaCreate


def get_media(db: Session, media_id: int):
    return db.query(Media).filter(Media.id == media_id).first()


def get_chat_medias(db: Session, chat_id: int, skip: int = 0, limit: int = 20):
    return db.query(Media).filter(
        Media.chat_id == chat_id
    ).order_by(Media.created_at.desc()).offset(skip).limit(limit).all()


def create_media(db: Session, chat_id: int, user_id: int, data: MediaCreate):
    db_media = Media(
        chat_id=chat_id,
        user_id=user_id,
        type=data.type,
        url=data.url,
        file_name=data.file_name,
        file_size=data.file_size,
        duration=data.duration
    )
    db.add(db_media)
    db.commit()
    db.refresh(db_media)
    return db_media


def delete_media(db: Session, media_id: int):
    db_media = get_media(db, media_id)
    if db_media:
        db.delete(db_media)
        db.commit()