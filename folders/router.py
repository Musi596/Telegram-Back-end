from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from folders import crud, schemas
from folder_chats.crud import get_folder_chats, add_chat_to_folder, remove_chat_from_folder
from chats.crud import get_chat
from auth.crud import get_current_user
from users.models import User

router = APIRouter(prefix="/folders", tags=["folders"])


@router.get("/", response_model=list[schemas.FolderResponse])
def get_folders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.get_user_folders(db, current_user.id)


@router.post("/", response_model=schemas.FolderResponse, status_code=status.HTTP_201_CREATED)
def create_folder(
    data: schemas.FolderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.create_folder(db, current_user.id, data.name)


@router.put("/{folder_id}", response_model=schemas.FolderResponse)
def update_folder(
    folder_id: int,
    data: schemas.FolderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    folder = crud.get_folder(db, folder_id)
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")
    if folder.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your folder")
    return crud.update_folder(db, folder_id, data.name)


@router.delete("/{folder_id}", status_code=204)
def delete_folder(
    folder_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    folder = crud.get_folder(db, folder_id)
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")
    if folder.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your folder")
    crud.delete_folder(db, folder_id)


@router.post("/{folder_id}/chats", status_code=status.HTTP_201_CREATED)
def add_chat(
    folder_id: int,
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    folder = crud.get_folder(db, folder_id)
    if not folder or folder.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Folder not found")
    chat = get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    add_chat_to_folder(db, folder_id, chat_id)
    return {"detail": "Chat added to folder"}


@router.delete("/{folder_id}/chats/{chat_id}", status_code=204)
def remove_chat(
    folder_id: int,
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    folder = crud.get_folder(db, folder_id)
    if not folder or folder.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Folder not found")
    remove_chat_from_folder(db, folder_id, chat_id)