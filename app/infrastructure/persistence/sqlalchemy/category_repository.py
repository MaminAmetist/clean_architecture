from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# Импортируем чистую доменную модель и интерфейс
from app.domain.models.category import Category
from app.domain.repositories.categories import ICategoryRepository
# Импортируем ORM-модель
from app.infrastructure.persistence.sqlalchemy.models import CategoryORM


class SQLAlchemyCategoryRepository(ICategoryRepository):
    """
    Конкретная реализация ICategoryRepository для SQLAlchemy.
    Отвечает за преобразование между ORM-моделями и доменными сущностями.
    """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    def _to_domain_model(self, orm_model: CategoryORM) -> Category:
        """Преобразует SQLAlchemy ORM-модель в чистую доменную модель."""
        return Category(id=orm_model.id, name=orm_model.name)

    def _to_orm_model(self, domain_model: Category) -> CategoryORM:
        """Преобразует чистую доменную модель в SQLAlchemy ORM-модель."""
        # Для создания: id может быть None. SQLAlchemy сам сгенерирует.
        # Для обновления: id должен быть установлен.
        return CategoryORM(id=domain_model.id, name=domain_model.name)

    async def get_by_id(self, category_id: int) -> Category | None:
        orm_category = await self.db_session.scalar(
            select(CategoryORM).where(CategoryORM.id == category_id))
        if orm_category is None:
            return None
        return self._to_domain_model(orm_category)

    async def get_by_name(self, name: str) -> Category | None:
        orm_category = await self.db_session.scalar(
            select(CategoryORM).where(CategoryORM.name == name))
        if orm_category is None:
            return None
        return self._to_domain_model(orm_category)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Category]:
        orm_categories = await self.db_session.scalars(select(CategoryORM).offset(skip).limit(limit))
        return [self._to_domain_model(cat) for cat in orm_categories.all()]

    async def create(self, category: Category) -> Category:
        db_category_orm = self._to_orm_model(category)  # Преобразуем доменную в ORM
        self.db_session.add(db_category_orm)
        await self.db_session.commit()
        await self.db_session.refresh(db_category_orm)
        return self._to_domain_model(db_category_orm)  # Преобразуем ORM обратно в доменную
