from datetime import datetime
from uuid import UUID,uuid4

from sqlalchemy import Boolean ,String,DateTime
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True),primary_key=True,default=uuid4)

    username: Mapped[str] = mapped_column( String(50), unique= True,nullable= False)

    email: Mapped[str] = mapped_column( String(250),unique= True, nullable= False,index= True)

    password: Mapped[str] = mapped_column(String(255),nullable= False)

    is_active: Mapped[bool] = mapped_column(Boolean,nullable=False,default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow,nullable= False)

    updated_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable= False)

    is_verified: Mapped[bool] = mapped_column(Boolean,nullable= False, default= False)


    tokens = relationship(
    "UserToken",
    back_populates="user",
)


    



