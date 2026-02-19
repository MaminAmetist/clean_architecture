from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.schemas.post import PostCreate, PostRead
from app.application.services.post_service import PostService
from app.presentation.dependencies import get_post_service

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post_route(
        post_data: PostCreate,
        post_service: PostService = Depends(get_post_service)
):
    """Создать новый пост."""
    try:
        new_post_domain = await post_service.create_post(post_data)
        return PostRead.model_validate(new_post_domain)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"An unexpected error occurred: {e}")


@router.get("/{post_id}", response_model=PostRead)
async def get_post_by_id_route(
        post_id: int,
        post_service: PostService = Depends(get_post_service)
):
    """Получить пост по ID."""
    post_domain = await post_service.get_post_by_id(post_id)
    if not post_domain:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return PostRead.model_validate(post_domain)


@router.get("/", response_model=List[PostRead])
async def get_all_posts_route(
        skip: int = 0,
        limit: int = 100,
        post_service: PostService = Depends(get_post_service)
):
    """Получить список всех постов."""
    posts_domain = await post_service.get_all_posts(skip=skip, limit=limit)
    return [PostRead.model_validate(p) for p in posts_domain]
