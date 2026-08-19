from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from reactions import crud, schemas
from messages.crud import get_message
from members.crud import is_member
from auth.crud import get_current_user
from users.crud import get_user
from users.models import User

router = APIRouter(prefix="/messages", tags=["reactions"])


@router.post("/{message_id}/reactions", status_code=status.HTTP_201_CREATED)
def add_reaction(
    message_id: int,
    data: schemas.ReactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    message = get_message(db, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    if not is_member(db, message.chat_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not a member")
    reaction = crud.add_reaction(db, message_id, current_user.id, data.emoji)
    return {
        "id": reaction.id,
        "message_id": reaction.message_id,
        "user": get_user(db, reaction.user_id),
        "emoji": reaction.emoji,
        "created_at": reaction.created_at
    }


@router.delete("/{message_id}/reactions/{emoji}", status_code=204)
def remove_reaction(
    message_id: int,
    emoji: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    message = get_message(db, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    crud.remove_reaction(db, message_id, current_user.id, emoji)


@router.get("/{message_id}/reactions")
def get_reactions(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    message = get_message(db, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    reactions = crud.get_message_reactions(db, message_id)
    return [
        {
            "id": r.id,
            "message_id": r.message_id,
            "user": get_user(db, r.user_id),
            "emoji": r.emoji,
            "created_at": r.created_at
        }
        for r in reactions
    ]