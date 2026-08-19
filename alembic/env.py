from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from database import Base

from users import models as users_models
from contacts import models as contacts_models
from blocks import models as blocks_models
from user_settings import models as user_settings_models
from chats import models as chats_models
from members import models as members_models
from invite_links import models as invite_links_models
from medias import models as medias_models
from messages import models as messages_models
from reads import models as reads_models
from reactions import models as reactions_models
from pins import models as pins_models
from calls import models as calls_models
from bots import models as bots_models
from folders import models as folders_models
from folder_chats import models as folder_chats_models
from stories import models as stories_models
from story_views import models as story_views_models
from notifications import models as notifications_models

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()