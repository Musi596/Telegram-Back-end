from sqlalchemy.orm import Session
from notifications.models import Notification


def get_notification(db: Session, notification_id: int):
    return db.query(Notification).filter(Notification.id == notification_id).first()


def get_user_notifications(db: Session, user_id: int, skip: int = 0, limit: int = 20):
    return db.query(Notification).filter(
        Notification.to_user_id == user_id
    ).order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()


def get_unread_count(db: Session, user_id: int):
    return db.query(Notification).filter(
        Notification.to_user_id == user_id,
        Notification.is_read == False
    ).count()


def create_notification(db: Session, to_user_id: int, from_user_id: int, type: str, entity_id: int = None):
    if to_user_id == from_user_id:
        return None
    db_notification = Notification(
        to_user_id=to_user_id,
        from_user_id=from_user_id,
        type=type,
        entity_id=entity_id
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification


def mark_as_read(db: Session, notification_id: int):
    db_notification = get_notification(db, notification_id)
    if db_notification:
        db_notification.is_read = True
        db.commit()
        db.refresh(db_notification)
    return db_notification


def mark_all_as_read(db: Session, user_id: int):
    db.query(Notification).filter(
        Notification.to_user_id == user_id,
        Notification.is_read == False
    ).update({"is_read": True})
    db.commit()


def delete_notification(db: Session, notification_id: int):
    db_notification = get_notification(db, notification_id)
    if db_notification:
        db.delete(db_notification)
        db.commit()


def delete_all_notifications(db: Session, user_id: int):
    db.query(Notification).filter(
        Notification.to_user_id == user_id
    ).delete()
    db.commit()