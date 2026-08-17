from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
from config import DATABASE_URL


engine = create_engine(DATABASE_URL)


TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)