
from sqlalchemy.orm import sessionmaker,DeclarativeBase
from sqlalchemy import create_engine
from config import DATABASE_URL

engine=create_engine(DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

class Base(DeclarativeBase):
    pass




        
