from fastapi import Depends

# Импортируем сервисы из слоя Application
from app.application.services.category_service import CategoryService
from app.application.services.post_service import PostService
# Импортируем "фабрики" сервисов из инфраструктурного слоя
# (которые сами собирают зависимости для сервисов)
from app.infrastructure.database.dependencies import (
    get_category_service_impl,
    get_post_service_impl
)


def get_category_service(
        service: CategoryService = Depends(get_category_service_impl)
) -> CategoryService:
    return service


def get_post_service(
        service: PostService = Depends(get_post_service_impl)
) -> PostService:
    return service
