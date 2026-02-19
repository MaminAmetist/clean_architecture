from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Импортируем сервисы из Application Layer
from app.application.services.category_service import CategoryService
from app.application.services.post_service import PostService
# Импортируем интерфейсы из Domain Layer
from app.domain.repositories.categories import ICategoryRepository
from app.domain.repositories.posts import IPostRepository
# Импортируем фабрику сессий из infrastructure/database/connection.py
from app.infrastructure.database.connection import AsyncSessionLocal
# Импортируем конкретные реализации репозиториев из Infrastructure Layer
from app.infrastructure.persistence.sqlalchemy.category_repository import \
    SQLAlchemyCategoryRepository
from app.infrastructure.persistence.sqlalchemy.post_repository import SQLAlchemyPostRepository


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Зависимость для предоставления асинхронной сессии БД"""
    async with AsyncSessionLocal() as session:
        yield session


def get_category_repository_impl(
        db_session: AsyncSession = Depends(get_db_session)
) -> ICategoryRepository:
    """Зависимость для предоставления конкретной реализации CategoryRepository"""
    return SQLAlchemyCategoryRepository(db_session)


def get_post_repository_impl(
        db_session: AsyncSession = Depends(get_db_session)
) -> IPostRepository:
    """Зависимость для предоставления конкретной реализации PostRepository"""
    return SQLAlchemyPostRepository(db_session)


def get_category_service_impl(
        category_repo: ICategoryRepository = Depends(get_category_repository_impl)
) -> CategoryService:
    """Зависимость для предоставления CategoryService"""
    return CategoryService(category_repo=category_repo)


def get_post_service_impl(
        post_repo: IPostRepository = Depends(get_post_repository_impl),
        category_repo: ICategoryRepository = Depends(get_category_repository_impl)
        # Используем общую зависимость
) -> PostService:
    """Зависимость для предоставления PostService"""
    return PostService(post_repo=post_repo, category_repo=category_repo)
