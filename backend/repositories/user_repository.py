from sqlalchemy.orm import Session
from models.user import User

def get_user_by_email(db:Session,email:str):
    return (db.query(User).filter(User.email==email).first())

def get_user_by_username(db:Session,username:str):
    return (
        db.query(User).filter(User.username==username).first()
    )

def create_user(db:Session,user:User):
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def verify_user(db: Session,user: User):
    user.is_verified = True

    db.commit()
    db.refresh(user)

    return user

def get_user_by_id(
    db: Session,
    user_id: str,
):
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )
