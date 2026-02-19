from abc import ABC, abstractmethod
from collections.abc import Sequence

from app.domain.models.post import Post  # Работаем с чистой доменной моделью


class IPostRepository(ABC):
    """
    Интерфейс репозитория для сущности Post.
    Определяет контракт для работы с данными постов.
    """

    @abstractmethod
    async def get_by_id(self, post_id: int) -> Post | None:
        pass

    @abstractmethod
    async def get_by_category_id(self, category_id: int, skip: int = 0, limit: int = 100) -> Sequence[Post]:
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[Post]:
        pass

    @abstractmethod
    async def create(self, post: Post) -> Post:
        pass
