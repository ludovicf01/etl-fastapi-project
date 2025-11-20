"""session service"""
from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session
from sqlmodel import create_engine as create_engine_bis
from app.config import settings

engine = create_engine_bis(settings.DATABASE_URL, pool_pre_ping=True)


def create_db_and_tables():
    """create db"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """get session"""
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
