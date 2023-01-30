from typing import List, Union

from pydantic import BaseModel

class TodoItemBase(BaseModel):
    title: str
    description: Union[str, None] = None
    is_on: bool = True

class TodoItemCreate(TodoItemBase):
    pass


class TodoItem(TodoItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class TodoItemUpdate(TodoItemBase):
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[TodoItem] = []

    class Config:
        orm_mode = True
