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


class TodoItemTagBase(BaseModel):
    tag_name: str


class TodoItemTag(TodoItemTagBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class TodoItemTagCreate(TodoItemTagBase):
    pass


class User(UserBase):
    id: int
    is_active: bool
    items: List[TodoItem] = []

    class Config:
        orm_mode = True


class TodoListBase(BaseModel):
    list_name: str
    date: str


class TodoList(TodoListBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class TodoListCreate(TodoListBase):
    pass