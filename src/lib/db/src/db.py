
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.declarative import declarative_base

from settings import DB_URI
from settings import DB_ECHO


engine = create_engine(DB_URI, convert_unicode=True, echo=DB_ECHO, poolclass=NullPool)

Session = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=True,
        expire_on_commit=False)
session = scoped_session(Session)

Model = declarative_base()

