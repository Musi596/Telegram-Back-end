from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from bots import crud, schemas
from auth.crud import get_current_user
from users.models import User

router = APIRouter(prefix="/bots", tags=["bots"])


@router.post("/", response_model=schemas.BotResponse, status_code=status.HTTP_201_CREATED)
def create_bot(
    data: schemas.BotCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bot = crud.create_bot(db, current_user.id, data.name, data.username, data.description)
    return bot


@router.get("/", response_model=list[schemas.BotShort])
def get_my_bots(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.get_user_bots(db, current_user.id)


@router.get("/{bot_id}", response_model=schemas.BotResponse)
def get_bot(
    bot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bot = crud.get_bot(db, bot_id)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    if bot.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your bot")
    return bot


@router.delete("/{bot_id}", status_code=204)
def delete_bot(
    bot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bot = crud.get_bot(db, bot_id)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    if bot.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your bot")
    crud.delete_bot(db, bot_id)