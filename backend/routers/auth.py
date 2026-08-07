from fastapi import APIRouter,status,Depends,Query
from schemas import UserCreate
from sqlalchemy.orm import Session
from services.email_service import send_verification_email
from services.auth_service import register_user
from dependencies import get_db
from services.email_verification_service import verify_email



router = APIRouter(prefix= "/auth",tags=["Authentication"])

@router.get("/test")
def test():
    return {
        "message": "Authetication is working"
    }

@router.post("/register",status_code=status.HTTP_201_CREATED)
async def register(user:UserCreate,db:Session = Depends(get_db)):
    return await register_user(user,db)


@router.get("/verify-email")
def verify_email_route(
    token: str = Query(...),
    db: Session = Depends(get_db),
):
    return verify_email(
        db=db,
        token=token,
    )
