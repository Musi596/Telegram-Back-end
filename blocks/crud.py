from sqlalchemy.orm import Session
from blocks.models import Block


def get_block(db: Session, user_id: int, blocked_id: int):
    return db.query(Block).filter(
        Block.user_id == user_id,
        Block.blocked_id == blocked_id
    ).first()


def get_blocked_users(db: Session, user_id: int):
    return db.query(Block).filter(Block.user_id == user_id).all()


def get_blocked_ids(db: Session, user_id: int):
    blocks = db.query(Block).filter(Block.user_id == user_id).all()
    return [b.blocked_id for b in blocks]


def is_blocked(db: Session, user_id: int, blocked_id: int):
    return get_block(db, user_id, blocked_id) is not None


def block_user(db: Session, user_id: int, blocked_id: int):
    existing = get_block(db, user_id, blocked_id)
    if existing:
        return existing
    db_block = Block(user_id=user_id, blocked_id=blocked_id)
    db.add(db_block)
    db.commit()
    db.refresh(db_block)
    return db_block


def unblock_user(db: Session, user_id: int, blocked_id: int):
    db_block = get_block(db, user_id, blocked_id)
    if db_block:
        db.delete(db_block)
        db.commit()