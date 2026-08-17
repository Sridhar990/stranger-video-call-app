from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base

TEST_DATABASE_URL = (
    "postgresql://app_user:change_this_local_password@localhost:5433/stranger_video_call_test"
)

engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)