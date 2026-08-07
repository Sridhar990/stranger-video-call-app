from sqlalchemy.orm import Session
from models import UserToken



def create_user_token(db: Session,user_token: UserToken):
    db.add(user_token)
    db.commit()
    db.refresh(user_token)

    return user_token

def get_token(db:Session,token: str):
    return (db.query(UserToken).filter(UserToken.token==token).first())

def mark_token_as_used(
    db: Session,
    user_token: UserToken,
):
    user_token.used = True

    db.commit()
    db.refresh(user_token)

    return user_token
