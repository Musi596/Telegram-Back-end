from fastapi import FastAPI
from database import Base, engine
from auth.router import router as auth_router
from users.router import router as users_router
from contacts.router import router as contacts_router
from blocks.router import router as blocks_router
from user_settings.router import router as settings_router
from chats.router import router as chats_router
from members.router import router as members_router
from invite_links.router import router as invite_links_router
from messages.router import router as messages_router
from reactions.router import router as reactions_router
from pins.router import router as pins_router
from medias.router import router as medias_router
from calls.router import router as calls_router
from bots.router import router as bots_router
from folders.router import router as folders_router
from stories.router import router as stories_router
from notifications.router import router as notifications_router
from fastapi.openapi.utils import get_openapi

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Telegram API", version="1.0.0")

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(contacts_router)
app.include_router(blocks_router)
app.include_router(settings_router)
app.include_router(chats_router)
app.include_router(members_router)
app.include_router(invite_links_router)
app.include_router(messages_router)
app.include_router(reactions_router)
app.include_router(pins_router)
app.include_router(medias_router)
app.include_router(calls_router)
app.include_router(bots_router)
app.include_router(folders_router)
app.include_router(stories_router)
app.include_router(notifications_router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Telegram API",
        version="1.0.0",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/")
def root():
    return {"message": "Telegram API is running"}