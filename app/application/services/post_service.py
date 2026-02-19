from typing import List

from app.application.schemas.post import PostCreate
from app.domain.models.post import Post
from app.domain.repositories.categories import ICategoryRepository
from app.domain.repositories.posts import IPostRepository


class PostService:
    def __init__(self, post_repo: IPostRepository, category_repo: ICategoryRepository):
        self.post_repo = post_repo
        self.category_repo = category_repo

    async def get_post_by_id(self, post_id: int) -> Post | None:
        return await self.post_repo.get_by_id(post_id)

    async def get_all_posts(self, skip: int = 0, limit: int = 100) -> List[Post]:
        return await self.post_repo.get_all(skip, limit)

    async def get_posts_by_category_id(self, category_id: int, skip: int = 0, limit: int = 100) -> \
            List[Post]:
        return await self.post_repo.get_by_category_id(category_id, skip, limit)

    async def create_post(self, post_data: PostCreate) -> Post:
        # Проверка существования категории
        category = await self.category_repo.get_by_id(post_data.category_id)
        if not category:
            raise ValueError(f"Category with ID {post_data.category_id} does not exist.")

        # Создаем чистую доменную модель
        new_post = Post(
            title=post_data.title,
            content=post_data.content,
            category_id=post_data.category_id
        )
        return await self.post_repo.create(new_post)
