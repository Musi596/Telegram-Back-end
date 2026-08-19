from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from contacts import crud, schemas
from auth.crud import get_current_user
from users.crud import get_user
from users.schemas import UserShort
from users.models import User

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=list[schemas.ContactResponse])
def get_contacts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contacts = crud.get_contacts(db, current_user.id)
    return [
        {
            "id": c.id,
            "user": get_user(db, c.contact_id),
            "name": c.name,
            "created_at": c.created_at
        }
        for c in contacts
    ]


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_contact(
    data: schemas.ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if data.contact_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot add yourself")
    target = get_user(db, data.contact_id)
    if not target:
        raise HTTPException(status_code=404, detail="User not found")
    crud.create_contact(db, current_user.id, data.contact_id, data.name)
    return {"detail": "Contact added"}


@router.delete("/{contact_id}", status_code=204)
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    crud.delete_contact(db, current_user.id, contact_id)