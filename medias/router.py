from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from medias import crud, schemas
from chats.crud import get_chat
from members.crud import is_member
from auth.crud import get_current_user
from users.crud import get_user
from users.models import User

router = APIRouter(prefix="/medias", tags=["medias"])


@router.post("/{chat_id}", status_code=status.HTTP_201_CREATED)
def upload_media(
    chat_id: int,
    data: schemas.MediaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat = get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if not is_member(db, chat_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not a member")
    media = crud.create_media(db, chat_id, current_user.id, data)
    return {
        "id": media.id,
        "chat_id": media.chat_id,
        "user": get_user(db, media.user_id),
        "type": media.type,
        "url": media.url,
        "file_name": media.file_name,
        "file_size": media.file_size,
        "duration": media.duration,
        "created_at": media.created_at
    }


@router.get("/{chat_id}")
def get_chat_medias(
    chat_id: int,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat = get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if not is_member(db, chat_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not a member")
    medias = crud.get_chat_medias(db, chat_id, skip, limit)
    return [
        {
            "id": m.id,
            "chat_id": m.chat_id,
            "user": get_user(db, m.user_id),
            "type": m.type,
            "url": m.url,
            "file_name": m.file_name,
            "file_size": m.file_size,
            "duration": m.duration,
            "created_at": m.created_at
        }
        for m in medias
    ]