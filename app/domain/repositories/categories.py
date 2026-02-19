from abc import ABC, abstractmethod
from collections.abc import Sequence

from app.domain.models.category import Category  # Работаем с чистой доменной моделью


class ICategoryRepository(ABC):
    """
    Интерфейс репозитория для сущности Category.
    Определяет контракт для работы с данными категорий.
    """

    @abstractmethod
    async def get_by_id(self, category_id: int) -> Category | None:
        pass

    @abstractmethod
    async def get_by_name(self, name: str) -> Category | None:
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[Category]:
        pass

    @abstractmethod
    async def create(self, category: Category) -> Category:
        pass
