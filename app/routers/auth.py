from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, oauth2, utils
from app.database import get_db
from app.schemas import Token, TokenData, UserLogin


router = APIRouter(
    tags=["Auth"]
)

@router.post("/login", response_model=Token)
def login_user(payload:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == payload.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid username or password")
    
    if not utils.verify(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid username or password")
    
    access_token = oauth2.create_access_token(data={"user_id":user.id, "user_email":user.email})
    print("access-tokenn:", access_token)
    return Token(access_token=access_token, token_type="bearer")