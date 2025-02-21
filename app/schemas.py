from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
import uuid



# Модель для входных данных авторизации
class AuthLogin(BaseModel):
    login: str
    password: str

# Модель для выходных данных авторизации
class AuthResponse(BaseModel):
    status: str
    access_token: Optional[str]

# Модель для создания/обновления пользователя
class UserCreate(BaseModel):
    login: str
    password: str
    fio: str

class UserUpdate(BaseModel):
    fio: str

class UserResponse(BaseModel):
    uuid: uuid.UUID
    login: str
    fio: str


# Модель для создания оборудования
class DeviceCreate(BaseModel):
    ip_address: str
    description: Optional[str]

class DeviceResponse(BaseModel):
    id: uuid.UUID
    ip_address: str
    description: Optional[str]

# Модель для создания абонентского терминала
class TerminalCreate(BaseModel):
    device_uuid: uuid.UUID
    mac: str
    model: str

class TerminalResponse(BaseModel):
    uuid: uuid.UUID
    mac: str
    model: str
    dt_created: datetime
    dt_last_pool: Optional[datetime]