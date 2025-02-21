from .main import app
from .database import Base, engine


# Создаем все таблицы в базе данных
Base.metadata.create_all(bind=engine)

# Экспорт app для использования в других местах
__all__ = ["app"]
