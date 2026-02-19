from dataclasses import dataclass
from typing import Optional


@dataclass
class Category:
    # Обязательные аргументы (без значения по умолчанию) должны идти первыми
    name: str
    # Затем идут необязательные аргументы (со значением по умолчанию)
    id: Optional[int] = None

    # Здесь также может быть доменная логика, если таковая имеется
