from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    todo_items = relationship("TodoItem", back_populates="owner")
    tags = relationship("TodoItemTag", back_populates="owner")
    todo_lists = relationship("TodoItemList", back_populates="owner")


class TodoItem(Base):
    __tablename__ = "todo_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    is_on = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    tag_id = Column(Integer, ForeignKey("todo_item_tags.id"))
    list_id = Column(Integer, ForeignKey("todo_item_lists.id"))

    owner = relationship("User", back_populates="todo_items")


class TodoItemTag(Base):
    __tablename__ = "todo_item_tags"

    id = Column(Integer, primary_key=True, index=True)
    tag_name = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="tags")


class TodoItemList(Base):
    __tablename__ = "todo_item_lists"

    id = Column(Integer, primary_key=True, index=True)
    list_name = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="todo_lists")