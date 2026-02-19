from dataclasses import dataclass
from typing import Optional


@dataclass
class Post:
    title: str
    content: str
    category_id: int

    id: Optional[int] = None  # ID будет None до сохранения
