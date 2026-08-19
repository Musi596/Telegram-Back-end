from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from notifications import crud, schemas
from auth.crud import get_current_user
from users.crud import get_user
from users.models import User

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("/")
def get_notifications(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notifications = crud.get_user_notifications(db, current_user.id, skip, limit)
    return [
        {
            "id": n.id,
            "from_user": get_user(db, n.from_user_id),
            "type": n.type,
            "entity_id": n.entity_id,
            "is_read": n.is_read,
            "created_at": n.created_at
        }
        for n in notifications
    ]


@router.get("/unread/count")
def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return {"unread_count": crud.get_unread_count(db, current_user.id)}


@router.put("/{notification_id}/read")
def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notification = crud.get_notification(db, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    if notification.to_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your notification")
    crud.mark_as_read(db, notification_id)
    return {"detail": "Marked as read"}


@router.put("/read/all")
def mark_all_as_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    crud.mark_all_as_read(db, current_user.id)
    return {"detail": "All marked as read"}


@router.delete("/{notification_id}", status_code=204)
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notification = crud.get_notification(db, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    if notification.to_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your notification")
    crud.delete_notification(db, notification_id)


@router.delete("/all", status_code=204)
def delete_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    crud.delete_all_notifications(db, current_user.id)