from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.schemas.category import CategoryCreate, CategoryRead
from app.application.services.category_service import CategoryService
from app.presentation.dependencies import get_category_service

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category_route(
        category_data: CategoryCreate,
        category_service: CategoryService = Depends(get_category_service)
):
    """Создать новую категорию."""
    try:
        new_category_domain = await category_service.create_category(category_data)
        return CategoryRead.model_validate(new_category_domain)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"An unexpected error occurred: {e}")


@router.get("/{category_id}", response_model=CategoryRead)
async def get_category_by_id_route(
        category_id: int,
        category_service: CategoryService = Depends(get_category_service)
):
    """Получить категорию по ID."""
    category_domain = await category_service.get_category_by_id(category_id)
    if not category_domain:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return CategoryRead.model_validate(category_domain)


@router.get("/", response_model=List[CategoryRead])
async def get_all_categories_route(
        skip: int = 0,
        limit: int = 100,
        category_service: CategoryService = Depends(get_category_service)
):
    """Получить список всех категорий."""
    categories_domain = await category_service.get_all_categories(skip=skip, limit=limit)
    return [CategoryRead.model_validate(cat) for cat in categories_domain]
