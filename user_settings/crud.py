from sqlalchemy.orm import Session
from user_settings.models import UserSettings
from user_settings.schemas import UserSettingsUpdate


def get_settings(db: Session, user_id: int):
    return db.query(UserSettings).filter(UserSettings.user_id == user_id).first()


def create_settings(db: Session, user_id: int):
    db_settings = UserSettings(user_id=user_id)
    db.add(db_settings)
    db.commit()
    db.refresh(db_settings)
    return db_settings


def get_or_create_settings(db: Session, user_id: int):
    settings = get_settings(db, user_id)
    if not settings:
        settings = create_settings(db, user_id)
    return settings


def update_settings(db: Session, user_id: int, data: UserSettingsUpdate):
    db_settings = get_or_create_settings(db, user_id)
    for key, value in data.model_dump(exclude_none=True).items():
        setattr(db_settings, key, value)
    db.commit()
    db.refresh(db_settings)
    return db_settings