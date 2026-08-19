from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from calls import crud, schemas
from auth.crud import get_current_user
from users.crud import get_user
from users.models import User

router = APIRouter(prefix="/calls", tags=["calls"])


def build_call(db, call):
    return {
        "id": call.id,
        "caller": get_user(db, call.caller_id),
        "receiver": get_user(db, call.receiver_id),
        "type": call.type,
        "status": call.status,
        "started_at": call.started_at,
        "ended_at": call.ended_at,
        "created_at": call.created_at
    }


@router.post("/", status_code=status.HTTP_201_CREATED)
def start_call(
    data: schemas.CallCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if data.receiver_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot call yourself")
    receiver = get_user(db, data.receiver_id)
    if not receiver:
        raise HTTPException(status_code=404, detail="User not found")
    call = crud.create_call(db, current_user.id, data.receiver_id, data.type)
    return build_call(db, call)


@router.put("/{call_id}/end")
def end_call(
    call_id: int,
    data: schemas.CallUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    call = crud.get_call(db, call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    if call.caller_id != current_user.id and call.receiver_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your call")
    call = crud.end_call(db, call_id, data.status)
    return build_call(db, call)


@router.get("/history")
def get_call_history(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    calls = crud.get_user_calls(db, current_user.id, skip, limit)
    return [build_call(db, call) for call in calls]