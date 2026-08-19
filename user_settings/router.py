from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from user_settings import crud, schemas
from auth.crud import get_current_user
from users.models import User

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("/", response_model=schemas.UserSettingsResponse)
def get_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.get_or_create_settings(db, current_user.id)


@router.put("/", response_model=schemas.UserSettingsResponse)
def update_settings(
    data: schemas.UserSettingsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.update_settings(db, current_user.id, data)