from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserResponse

router = APIRouter()

@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.get("/{userId}", response_model=UserResponse)
def get_user(userId: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == userId).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.delete("/{userId}", status_code=204)
def delete_user(userId: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == userId).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(user)
    db.commit()