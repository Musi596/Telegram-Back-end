from sqlalchemy.orm import Session
from folder_chats.models import FolderChat


def get_folder_chat(db: Session, folder_id: int, chat_id: int):
    return db.query(FolderChat).filter(
        FolderChat.folder_id == folder_id,
        FolderChat.chat_id == chat_id
    ).first()


def get_folder_chats(db: Session, folder_id: int):
    return db.query(FolderChat).filter(FolderChat.folder_id == folder_id).all()


def add_chat_to_folder(db: Session, folder_id: int, chat_id: int):
    existing = get_folder_chat(db, folder_id, chat_id)
    if existing:
        return existing
    db_fc = FolderChat(folder_id=folder_id, chat_id=chat_id)
    db.add(db_fc)
    db.commit()
    db.refresh(db_fc)
    return db_fc


def remove_chat_from_folder(db: Session, folder_id: int, chat_id: int):
    db_fc = get_folder_chat(db, folder_id, chat_id)
    if db_fc:
        db.delete(db_fc)
        db.commit()