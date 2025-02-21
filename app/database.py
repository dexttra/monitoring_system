from sqlalchemy import create_engine, Column, String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid as uuid_lib
from datetime import datetime


# Создаем базовый класс для моделей
Base = declarative_base()

# Модель для токенов авторизации
class AuthToken(Base):
    __tablename__ = 'auth_tokens'
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid_lib.uuid4)
    user_uuid = Column(UUID(as_uuid=True), ForeignKey('users.uuid'), nullable=False)
    access_token = Column(String, nullable=False)
    expire = Column(DateTime, nullable=False)

# Модель для пользователей
class User(Base):
    __tablename__ = 'users'
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid_lib.uuid4)
    login = Column(String, unique=True, nullable=False)
    pswd = Column(String, nullable=False)  # Хэш пароля
    fio = Column(String, nullable=False)
    status = Column(Integer, nullable=False, default=0)  # 0 - активен, 3 - закрыт

# Модель для оборудования
class Device(Base):
    __tablename__ = 'devices'
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid_lib.uuid4)
    ip_address = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

# Модель для абонентских терминалов
class Terminal(Base):
    __tablename__ = 'terminals'
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid_lib.uuid4)
    device_uuid = Column(UUID(as_uuid=True), ForeignKey('devices.uuid'), nullable=False)
    mac = Column(String, unique=True, nullable=False)
    model = Column(String, nullable=False)
    dt_created = Column(DateTime, default=datetime.utcnow)
    dt_last_pool = Column(DateTime, nullable=True)

# Создаем движок и сессию для работы с базой данных
DATABASE_URL = "postgresql://postgres:12345@localhost/monitoring_system"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()