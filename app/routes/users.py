from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
import uuid
from passlib.context import CryptContext

router = APIRouter(prefix="/users", tags=["Users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_user = db.query(models.User).filter(models.User.user_email == user.user_email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(user_id=uuid.uuid4(), user_name=user.user_name, user_email=user.user_email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.user_id == str(user_id)).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: uuid.UUID, user: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.user_id == str(user_id)).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.user_name = user.user_name
    db_user.user_email = user.user_email
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
def delete_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.user_id == str(user_id)).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}
