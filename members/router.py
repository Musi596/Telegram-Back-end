from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from members import crud, schemas
from chats.crud import get_chat
from auth.crud import get_current_user
from users.crud import get_user
from users.models import User

router = APIRouter(prefix="/chats", tags=["members"])


@router.get("/{chat_id}/members", response_model=list[schemas.MemberResponse])
def get_members(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat = get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if not crud.is_member(db, chat_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not a member")
    members = crud.get_chat_members(db, chat_id)
    return [
        {
            "id": m.id,
            "user": get_user(db, m.user_id),
            "role": m.role,
            "can_send": m.can_send,
            "can_add_members": m.can_add_members,
            "can_pin": m.can_pin,
            "joined_at": m.joined_at
        }
        for m in members
    ]


@router.post("/{chat_id}/members", status_code=status.HTTP_201_CREATED)
def add_member(
    chat_id: int,
    data: schemas.MemberCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat = get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if not crud.is_admin(db, chat_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not an admin")
    target = get_user(db, data.user_id)
    if not target:
        raise HTTPException(status_code=404, detail="User not found")
    crud.add_member(db, chat_id, data.user_id)
    return {"detail": "Member added"}


@router.delete("/{chat_id}/members/{user_id}", status_code=204)
def remove_member(
    chat_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat = get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if not crud.is_admin(db, chat_id, current_user.id) and user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    crud.remove_member(db, chat_id, user_id)


@router.put("/{chat_id}/members/{user_id}")
def update_member(
    chat_id: int,
    user_id: int,
    data: schemas.MemberUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat = get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if chat.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not the owner")
    member = crud.update_member(db, chat_id, user_id, data)
    return {
        "id": member.id,
        "user": get_user(db, member.user_id),
        "role": member.role,
        "can_send": member.can_send,
        "can_add_members": member.can_add_members,
        "can_pin": member.can_pin,
        "joined_at": member.joined_at
    }