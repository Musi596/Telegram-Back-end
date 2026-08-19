from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from blocks import crud, schemas
from auth.crud import get_current_user
from users.crud import get_user
from users.schemas import UserShort
from users.models import User

router = APIRouter(prefix="/blocks", tags=["blocks"])


@router.get("/", response_model=list[schemas.BlockResponse])
def get_blocked(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    blocks = crud.get_blocked_users(db, current_user.id)
    return [{"id": b.id, "blocked": get_user(db, b.blocked_id), "created_at": b.created_at} for b in blocks]


@router.post("/{user_id}", status_code=status.HTTP_201_CREATED)
def block_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot block yourself")
    target = get_user(db, user_id)
    if not target:
        raise HTTPException(status_code=404, detail="User not found")
    crud.block_user(db, current_user.id, user_id)
    return {"detail": "User blocked"}


@router.delete("/{user_id}", status_code=204)
def unblock_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    crud.unblock_user(db, current_user.id, user_id)