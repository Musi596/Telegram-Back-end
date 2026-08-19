from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from messages import crud, schemas
from chats.crud import get_chat
from members.crud import is_member
from auth.crud import get_current_user
from users.crud import get_user
from users.models import User

router = APIRouter(prefix="/messages", tags=["messages"])


def build_message(db, m):
    return {
        "id": m.id,
        "chat_id": m.chat_id,
        "user": get_user(db, m.user_id),
        "text": m.text,
        "media_id": m.media_id,
        "reply_to_id": m.reply_to_id,
        "forward_from_id": m.forward_from_id,
        "is_edited": m.is_edited,
        "is_deleted": m.is_deleted,
        "created_at": m.created_at,
        "edited_at": m.edited_at
    }


@router.post("/{chat_id}", status_code=status.HTTP_201_CREATED)
def send_message(
    chat_id: int,
    data: schemas.MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat = get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if not is_member(db, chat_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not a member")
    message = crud.create_message(
        db,
        chat_id=chat_id,
        user_id=current_user.id,
        text=data.text,
        media_id=data.media_id,
        reply_to_id=data.reply_to_id
    )
    return build_message(db, message)


@router.put("/{message_id}")
def edit_message(
    message_id: int,
    data: schemas.MessageUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    message = crud.get_message(db, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    if message.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your message")
    message = crud.update_message(db, message_id, data.text)
    return build_message(db, message)


@router.delete("/{message_id}", status_code=204)
def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    message = crud.get_message(db, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    if message.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your message")
    crud.delete_message(db, message_id)


@router.post("/{message_id}/forward/{chat_id}", status_code=status.HTTP_201_CREATED)
def forward_message(
    message_id: int,
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    message = crud.get_message(db, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    chat = get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if not is_member(db, chat_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not a member of target chat")
    forwarded = crud.forward_message(db, message_id, chat_id, current_user.id)
    return build_message(db, forwarded)