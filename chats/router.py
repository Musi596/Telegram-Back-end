from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from database import get_db
from chats import crud, schemas
from members.crud import add_member, get_chat_members, is_member, is_admin, get_members_count
from messages.crud import get_chat_messages, create_message, get_last_message
from reads.crud import mark_all_read
from auth.crud import get_current_user
from users.crud import get_user
from users.models import User
from typing import Dict, List
import json

router = APIRouter(prefix="/chats", tags=["chats"])


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, chat_id: int):
        await websocket.accept()
        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = []
        self.active_connections[chat_id].append(websocket)

    def disconnect(self, websocket: WebSocket, chat_id: int):
        if chat_id in self.active_connections:
            self.active_connections[chat_id].remove(websocket)

    async def broadcast(self, chat_id: int, message: dict):
        if chat_id in self.active_connections:
            for connection in self.active_connections[chat_id]:
                await connection.send_text(json.dumps(message))


manager = ConnectionManager()


def build_chat_response(db, chat):
    owner = get_user(db, chat.owner_id)
    last_msg = get_last_message(db, chat.id)
    members_count = get_members_count(db, chat.id)
    return {
        "id": chat.id,
        "type": chat.type,
        "name": chat.name,
        "description": chat.description,
        "photo": chat.photo,
        "owner": owner,
        "is_public": chat.is_public,
        "username": chat.username,
        "members_count": members_count,
        "last_message": last_msg.text if last_msg else None,
        "created_at": chat.created_at
    }


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_chat(
    data: schemas.ChatCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat = crud.create_chat(
        db,
        owner_id=current_user.id,
        type=data.type,
        name=data.name,
        description=data.description,
        photo=data.photo,
        is_public=data.is_public,
        username=data.username
    )
    add_member(db, chat.id, current_user.id, role="owner")
    for member_id in data.member_ids:
        if member_id != current_user.id:
            add_member(db, chat.id, member_id)
    return build_chat_response(db, chat)


@router.get("/", )
def get_my_chats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chats = crud.get_user_chats(db, current_user.id)
    return [build_chat_response(db, chat) for chat in chats]


@router.get("/{chat_id}")
def get_chat(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat = crud.get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if not is_member(db, chat_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not a member")
    return build_chat_response(db, chat)


@router.put("/{chat_id}")
def update_chat(
    chat_id: int,
    data: schemas.ChatUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat = crud.get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if not is_admin(db, chat_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not an admin")
    chat = crud.update_chat(db, chat_id, data)
    return build_chat_response(db, chat)


@router.delete("/{chat_id}", status_code=204)
def delete_chat(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat = crud.get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if chat.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not the owner")
    crud.delete_chat(db, chat_id)


@router.get("/{chat_id}/messages")
def get_messages(
    chat_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat = crud.get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if not is_member(db, chat_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not a member")
    mark_all_read(db, chat_id, current_user.id)
    messages = get_chat_messages(db, chat_id, skip, limit)
    return [
        {
            "id": m.id,
            "chat_id": m.chat_id,
            "user": get_user(db, m.user_id),
            "text": m.text,
            "media_id": m.media_id,
            "reply_to_id": m.reply_to_id,
            "forward_from_id": m.forward_from_id,
            "is_edited": m.is_edited,
            "is_deleted": m.is_deleted,
            "created_at": m.created_at,
            "edited_at": m.edited_at
        }
        for m in messages
    ]


@router.get("/{chat_id}/unread")
def get_unread(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from reads.crud import get_unread_count
    chat = crud.get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if not is_member(db, chat_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not a member")
    return {"unread_count": get_unread_count(db, chat_id, current_user.id)}


@router.websocket("/{chat_id}/ws/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    chat_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    chat = crud.get_chat(db, chat_id)
    if not chat or not is_member(db, chat_id, user_id):
        await websocket.close(code=1008)
        return

    await manager.connect(websocket, chat_id)
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            message = create_message(
                db,
                chat_id=chat_id,
                user_id=user_id,
                text=payload.get("text"),
                media_id=payload.get("media_id"),
                reply_to_id=payload.get("reply_to_id")
            )
            user = get_user(db, user_id)
            await manager.broadcast(chat_id, {
                "id": message.id,
                "chat_id": chat_id,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "full_name": user.full_name,
                    "photo": user.photo,
                    "is_verified": user.is_verified
                },
                "text": message.text,
                "media_id": message.media_id,
                "reply_to_id": message.reply_to_id,
                "created_at": str(message.created_at)
            })
    except WebSocketDisconnect:
        manager.disconnect(websocket, chat_id)