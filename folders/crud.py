from sqlalchemy.orm import Session
from folders.models import Folder


def get_folder(db: Session, folder_id: int):
    return db.query(Folder).filter(Folder.id == folder_id).first()


def get_user_folders(db: Session, user_id: int):
    return db.query(Folder).filter(Folder.user_id == user_id).all()


def create_folder(db: Session, user_id: int, name: str):
    db_folder = Folder(user_id=user_id, name=name)
    db.add(db_folder)
    db.commit()
    db.refresh(db_folder)
    return db_folder


def update_folder(db: Session, folder_id: int, name: str):
    db_folder = get_folder(db, folder_id)
    db_folder.name = name
    db.commit()
    db.refresh(db_folder)
    return db_folder


def delete_folder(db: Session, folder_id: int):
    db_folder = get_folder(db, folder_id)
    if db_folder:
        db.delete(db_folder)
        db.commit()