from sqlalchemy.orm import Session
from passlib.context import CryptContext
from users.models import User
from users.schemas import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_phone(db: Session, phone: str):
    return db.query(User).filter(User.phone == phone).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def search_users(db: Session, query: str):
    return db.query(User).filter(
        User.username.ilike(f"%{query}%") |
        User.full_name.ilike(f"%{query}%") |
        User.phone.ilike(f"%{query}%")
    ).limit(20).all()


def create_user(db: Session, data: UserCreate):
    hashed_password = pwd_context.hash(data.password)
    db_user = User(
        phone=data.phone,
        password=hashed_password,
        username=data.username
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, data: UserUpdate):
    db_user = get_user(db, user_id)
    for key, value in data.model_dump(exclude_none=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    db.delete(db_user)
    db.commit()


def verify_password(plain_password:  str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
    