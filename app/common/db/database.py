import app.common.config.settings as conf
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

async_engine = create_engine(conf.DATABASE_URL)
Session = sessionmaker(async_engine)


class Base(DeclarativeBase):
    pass
