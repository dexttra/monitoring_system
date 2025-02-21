from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db, User
from app.schemas import UserCreate, UserUpdate, UserResponse
from app.auth import get_current_user, get_password_hash
from app.schemas import UserResponse
import uuid

router = APIRouter()

# Получение списка пользователей
@router.get("/users", response_model=list[UserResponse])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

# Создание нового пользователя
@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = User(login=user.login, pswd=hashed_password, fio=user.fio)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Обновление пользователя
@router.patch("/users/{user_uuid}", response_model=UserResponse)
def update_user(
    user_uuid: uuid.UUID,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Защита маршрута
):
    db_user = db.query(User).filter(User.uuid == user_uuid).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.fio = user_update.fio
    db.commit()
    db.refresh(db_user)
    return db_user

# Удаление пользователя
@router.delete("/users/{user_uuid}")
def delete_user(
    user_uuid: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Защита маршрута
):
    db_user = db.query(User).filter(User.uuid == user_uuid).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"status": "ok"}