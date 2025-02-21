from fastapi import FastAPI
from app.auth import router as auth_router
from app.users import router as users_router
from app.devices import router as devices_router
from app.terminals import router as terminals_router


app = FastAPI()

# Подключение роутеров
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(devices_router, prefix="/api/v1")
app.include_router(terminals_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Network Monitoring System!"}