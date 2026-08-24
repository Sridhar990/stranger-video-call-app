from sqlalchemy.orm import Session
from models import UserToken,TokenType



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



def revoke_all_refresh_tokens(
    db: Session,
    user_id,
):
    tokens = (
        db.query(UserToken)
        .filter(
            UserToken.user_id == user_id,
            UserToken.token_type == TokenType.REFRESH_TOKEN,
            UserToken.used == False,
        )
        .all()
    )

    for token in tokens:
        token.used = True

    db.commit()

    return tokens