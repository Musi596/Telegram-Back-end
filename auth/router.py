from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from auth import crud, schemas

router = APIRouter(prefix="/auth", tags=["auth"])
bearer_scheme = HTTPBearer()


@router.post("/register", response_model=schemas.Token, status_code=status.HTTP_201_CREATED)
def register(data: schemas.Register, db: Session = Depends(get_db)):
    user = crud.register(db, data)
    if not user:
        raise HTTPException(status_code=400, detail="Phone already registered")
    token = crud.create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=schemas.Token)
def login(data: schemas.Login, db: Session = Depends(get_db)):
    result = crud.login(db, data)
    if not result:
        raise HTTPException(status_code=401, detail="Invalid phone or password")
    return result


@router.post("/change-password")
def change_password(
    data: schemas.ChangePassword,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    current_user = crud.get_current_user(credentials, db)
    from users.crud import verify_password, pwd_context
    if not verify_password(data.old_password, current_user.password):
        raise HTTPException(status_code=400, detail="Wrong old password")
    current_user.password = pwd_context.hash(data.new_password)
    db.commit()
    return {"detail": "Password changed successfully"}