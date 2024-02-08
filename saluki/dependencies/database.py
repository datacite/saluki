from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from saluki.config import settings


engine = create_engine(
    settings.sqlalchemy_database_url, connect_args={"check_same_thread": False}
)
DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_database():
    """Provide a database session for dependency injection."""
    database = DBSession()
    try:
        yield database
    finally:
        database.close()
