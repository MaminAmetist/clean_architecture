from typing import List

from app.application.schemas.category import CategoryCreate
from app.domain.models.category import Category
from app.domain.repositories.categories import ICategoryRepository


class CategoryService:
    def __init__(self, category_repo: ICategoryRepository):
        self.category_repo = category_repo

    async def get_category_by_id(self, category_id: int) -> Category | None:
        """Получает категорию по ID (возвращает доменную модель)."""
        return await self.category_repo.get_by_id(category_id)

    async def get_category_by_name(self, name: str) -> Category | None:
        """Получает категорию по имени (возвращает доменную модель)."""
        return await self.category_repo.get_by_name(name)

    async def get_all_categories(self, skip: int = 0, limit: int = 100) -> List[Category]:
        """Получает список всех категорий (возвращает список доменных моделей)."""
        return await self.category_repo.get_all(skip, limit)

    async def create_category(self, category_data: CategoryCreate) -> Category:
        """Создает новую категорию, проверяя на уникальность имени."""
        existing_category = await self.category_repo.get_by_name(category_data.name)
        if existing_category:
            raise ValueError(f"Category with name '{category_data.name}' already exists.")
        # Создаем чистую доменную модель для передачи в репозиторий
        new_category = Category(name=category_data.name)
        return await self.category_repo.create(new_category)
