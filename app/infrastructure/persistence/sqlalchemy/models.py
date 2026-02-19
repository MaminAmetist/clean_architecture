from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.infrastructure.database.connection import Base


class CategoryORM(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    posts = relationship("PostORM", back_populates="category_rel")

    def __repr__(self):
        return f"<CategoryORM(id={self.id}, name='{self.name}')>"


class PostORM(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    content = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    category_rel = relationship("CategoryORM", back_populates="posts")

    def __repr__(self):
        return f"<PostORM(id={self.id}, title='{self.title}', category_id={self.category_id})>"
