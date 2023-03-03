from sqlalchemy.orm import Session

from . import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.TodoItemCreate, user_id: int):
    db_item = models.TodoItem(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TodoItem).offset(skip).limit(limit).all()


def update_user_item(db: Session, item: schemas.TodoItemUpdate, item_id: int):
    db_item = db.query(models.TodoItem).filter(models.TodoItem.id == item_id).first()
    db_item.title = item.title
    db_item.description = item.description
    db_item.is_on = item.is_on
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_user_item(db: Session, item_id: int):
    db_item = db.query(models.TodoItem).filter(models.TodoItem.id == item_id).first()
    db.delete(db_item)
    db.commit()
    return db_item


def create_user_tag(db: Session, tag: schemas.TodoItemTagCreate, user_id: int):
    db_tag = models.TodoItemTag(**tag.dict(), owner_id=user_id)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def get_tags(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TodoItemTag).offset(skip).limit(limit).all()


def update_user_tag(db: Session, tag: schemas.TodoItemTag, tag_id: int):
    db_tag = db.query(models.TodoItemTag).filter(models.TodoItemTag.id == tag_id).first()
    db_tag.tag_name = tag.tag_name
    db.commit()
    db.refresh(db_tag)
    return db_tag


def delete_user_tag(db: Session, tag_id: int):
    db_tag = db.query(models.TodoItemTag).filter(models.TodoItemTag.id == tag_id).first()
    db.delete(db_tag)
    db.commit()
    return db_tag


def create_todo_list(db: Session, todo_list: schemas.TodoListCreate, user_id: int):
    db_todo_list = models.TodoList(**todo_list.dict(), owner_id=user_id)
    db.add(db_todo_list)
    db.commit()
    db.refresh(db_todo_list)
    return db_todo_list


def get_todo_lists(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TodoList).offset(skip).limit(limit).all()