from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from invite_links import crud, schemas
from chats.crud import get_chat
from members.crud import is_admin, add_member, is_member
from auth.crud import get_current_user
from users.crud import get_user
from users.models import User

router = APIRouter(prefix="/chats", tags=["invite_links"])


@router.post("/{chat_id}/invite-links", status_code=status.HTTP_201_CREATED)
def create_invite_link(
    chat_id: int,
    data: schemas.InviteLinkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat = get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if not is_admin(db, chat_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not an admin")
    link = crud.create_invite_link(db, chat_id, current_user.id, data.expires_at)
    return {
        "id": link.id,
        "chat_id": link.chat_id,
        "created_by": get_user(db, link.created_by),
        "link": link.link,
        "is_active": link.is_active,
        "expires_at": link.expires_at,
        "created_at": link.created_at
    }


@router.get("/{chat_id}/invite-links")
def get_invite_links(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat = get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if not is_admin(db, chat_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not an admin")
    links = crud.get_chat_invite_links(db, chat_id)
    return [
        {
            "id": l.id,
            "chat_id": l.chat_id,
            "created_by": get_user(db, l.created_by),
            "link": l.link,
            "is_active": l.is_active,
            "expires_at": l.expires_at,
            "created_at": l.created_at
        }
        for l in links
    ]


@router.delete("/{chat_id}/invite-links/{link_id}", status_code=204)
def revoke_invite_link(
    chat_id: int,
    link_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat = get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if not is_admin(db, chat_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not an admin")
    crud.revoke_invite_link(db, link_id)


@router.post("/join/{link}", status_code=status.HTTP_200_OK)
def join_by_link(
    link: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_link = crud.get_invite_link(db, link)
    if not db_link or not db_link.is_active:
        raise HTTPException(status_code=404, detail="Invalid or expired link")
    if db_link.expires_at and db_link.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Link expired")
    if is_member(db, db_link.chat_id, current_user.id):
        raise HTTPException(status_code=400, detail="Already a member")
    add_member(db, db_link.chat_id, current_user.id)
    return {"detail": "Joined successfully", "chat_id": db_link.chat_id}