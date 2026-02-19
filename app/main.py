from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infrastructure.database.connection import create_db_and_tables
from app.presentation.routers import categories, posts


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Приложение запускается. Создаем базу данных...")
    await create_db_and_tables()
    print("База данных инициализирована.")
    yield
    print("Приложение завершает работу.")


app = FastAPI(title="My Blog API - Clean Architecture", lifespan=lifespan)

# Подключение роутеров
app.include_router(categories.router)
app.include_router(posts.router)


@app.get("/")
async def root():
    return {"message": "Welcome to My Blog API! Check /docs for OpenAPI documentation."}
