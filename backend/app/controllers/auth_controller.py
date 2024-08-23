from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserCreate
import bcrypt

router = APIRouter()

@router.post("/register", status_code=201)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    user.password = hashed_password.decode('utf-8')
    
    db_user = User(username=user.username, password=user.password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login")
async def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if user is None or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return {"message": "Inicio de sesión exitoso"}