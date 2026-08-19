from sqlalchemy.orm import Session
from contacts.models import Contact


def get_contact(db: Session, user_id: int, contact_id: int):
    return db.query(Contact).filter(
        Contact.user_id == user_id,
        Contact.contact_id == contact_id
    ).first()


def get_contacts(db: Session, user_id: int):
    return db.query(Contact).filter(Contact.user_id == user_id).all()


def create_contact(db: Session, user_id: int, contact_id: int, name: str = None):
    db_contact = Contact(user_id=user_id, contact_id=contact_id, name=name)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, user_id: int, contact_id: int):
    db_contact = get_contact(db, user_id, contact_id)
    if db_contact:
        db.delete(db_contact)
        db.commit()