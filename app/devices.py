from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db, Device
from app.schemas import DeviceCreate, DeviceResponse
from app.auth import get_current_user


router = APIRouter()

# Получение списка оборудования
@router.get("/devices", response_model=list[DeviceResponse])
def read_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    devices = db.query(Device).offset(skip).limit(limit).all()
    return devices

# Создание нового оборудования
@router.post("/devices", response_model=DeviceResponse)
def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
    db_device = Device(ip_address=device.ip_address, description=device.description)
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device