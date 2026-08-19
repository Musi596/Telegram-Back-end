from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from pins import crud, schemas
from chats.crud import get_chat
from messages.crud import get_message
from members.crud import is_member, is_admin
from auth.crud import get_current_user
from users.crud import get_user
from users.models import User

router = APIRouter(prefix="/chats", tags=["pins"])


@router.post("/{chat_id}/pin/{message_id}", status_code=status.HTTP_201_CREATED)
def pin_message(
    chat_id: int,
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat = get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if not is_admin(db, chat_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not an admin")
    message = get_message(db, message_id)
    if not message or message.chat_id != chat_id:
        raise HTTPException(status_code=404, detail="Message not found")
    pin = crud.pin_message(db, chat_id, message_id, current_user.id)
    return {"detail": "Message pinned", "pin_id": pin.id}


@router.delete("/{chat_id}/pin/{message_id}", status_code=204)
def unpin_message(
    chat_id: int,
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat = get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if not is_admin(db, chat_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not an admin")
    crud.unpin_message(db, chat_id, message_id)


@router.get("/{chat_id}/pin")
def get_pinned(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat = get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if not is_member(db, chat_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not a member")
    pin = crud.get_last_pin(db, chat_id)
    if not pin:
        raise HTTPException(status_code=404, detail="No pinned message")
    message = get_message(db, pin.message_id)
    return {
        "id": pin.id,
        "chat_id": pin.chat_id,
        "message": {
            "id": message.id,
            "text": message.text,
            "user": get_user(db, message.user_id),
            "created_at": message.created_at
        },
        "pinned_by": get_user(db, pin.pinned_by),
        "pinned_at": pin.pinned_at
    }