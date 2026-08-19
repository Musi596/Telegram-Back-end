from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from stories import crud, schemas
from auth.crud import get_current_user
from users.crud import get_user
from users.models import User

router = APIRouter(prefix="/stories", tags=["stories"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_story(
    data: schemas.StoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    story = crud.create_story(db, current_user.id, data.url, data.type)
    return {
        "id": story.id,
        "user": get_user(db, story.user_id),
        "url": story.url,
        "type": story.type,
        "expires_at": story.expires_at,
        "views_count": 0,
        "created_at": story.created_at
    }


@router.get("/user/{user_id}")
def get_user_stories(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stories = crud.get_user_stories(db, user_id)
    return [
        {
            "id": s.id,
            "user": get_user(db, s.user_id),
            "url": s.url,
            "type": s.type,
            "expires_at": s.expires_at,
            "views_count": crud.get_views_count(db, s.id),
            "created_at": s.created_at
        }
        for s in stories
    ]


@router.post("/{story_id}/view")
def view_story(
    story_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    story = crud.get_story(db, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    crud.view_story(db, story_id, current_user.id)
    return {"detail": "Viewed"}


@router.get("/{story_id}/views")
def get_story_views(
    story_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    story = crud.get_story(db, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    if story.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your story")
    views = crud.get_story_views(db, story_id)
    return [{"user": get_user(db, v.user_id), "viewed_at": v.viewed_at} for v in views]


@router.delete("/{story_id}", status_code=204)
def delete_story(
    story_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    story = crud.get_story(db, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    if story.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your story")
    crud.delete_story(db, story_id)