from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db, Terminal, Device, User  # Добавляем импорт User
from app.schemas import TerminalCreate, TerminalResponse
from app.auth import get_current_user  # Импортируем get_current_user для защиты маршрутов
from typing import List  # Импортируем List для использования в response_model
import uuid


router = APIRouter()

# Получение списка терминалов по ID оборудования
@router.get("/terminals/{device_uuid}", response_model=List[TerminalResponse])
def read_terminals(
    device_uuid: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Защита маршрута
):
    """
    Возвращает список абонентских терминалов, связанных с указанным оборудованием.
    """
    terminals = db.query(Terminal).filter(Terminal.device_uuid == device_uuid).all()
    if not terminals:
        raise HTTPException(status_code=404, detail="Terminals not found for the given device")
    return terminals

# Создание нового терминала
@router.post("/terminals", response_model=TerminalResponse)
def create_terminal(
    terminal: TerminalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Создает новый абонентский терминал и связывает его с указанным оборудованием.
    """
    # Проверяем, существует ли указанное оборудование
    device = db.query(Device).filter(Device.uuid == terminal.device_uuid).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    # Создаем новый терминал
    db_terminal = Terminal(
        device_uuid=terminal.device_uuid,
        mac=terminal.mac,
        model=terminal.model
    )
    db.add(db_terminal)
    db.commit()
    db.refresh(db_terminal)
    return db_terminal

# Удаление терминала
@router.delete("/terminals/{terminal_uuid}")
def delete_terminal(
    terminal_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Защита маршрута
):
    # Удаляет абонентский терминал по его ID.
    terminal = db.query(Terminal).filter(Terminal.id == terminal_uuid).first()
    if not terminal:
        raise HTTPException(status_code=404, detail="Terminal not found")
    db.delete(terminal)
    db.commit()
    return {"status": "ok"}