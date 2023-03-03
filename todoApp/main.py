from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .fastapi_utils_tasks import repeat_every
import datetime
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.TodoItem)
def create_item_for_user(
    user_id: int, item: schemas.TodoItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/todoitems/", response_model=List[schemas.TodoItem])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.put("/items/{item_id}", response_model=schemas.TodoItem)
def update_item(item_id: int, item: schemas.TodoItemUpdate, db: Session = Depends(get_db)):
    return crud.update_user_item(db=db, item_id=item_id, item=item)


@app.delete("/items/{item_id}", response_model=schemas.TodoItem)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    return crud.delete_user_item(db=db, item_id=item_id)


@app.post("/users/{user_id}/tags/", response_model=schemas.TodoItemTag)
def create_tag_for_user(
    user_id: int, tag: schemas.TodoItemTagCreate, db: Session = Depends(get_db)
):
    return crud.create_user_tag(db=db, tag=tag, user_id=user_id)


@app.get("/tags/", response_model=List[schemas.TodoItemTag])
def read_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tags = crud.get_tags(db, skip=skip, limit=limit)
    return tags


@app.get("/todolists/", response_model=List[schemas.TodoList])
def read_todolists(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todolists = crud.get_todo_lists(db, skip=skip, limit=limit)
    return todolists

# creating todolists on startup
@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    
    if(not crud.get_user(db, 1)):
        crud.create_user(db, schemas.UserCreate(email="test", password="test"))

    if(not crud.get_todo_lists(db, 1)):
        date = datetime.datetime.now().strftime("%d/%m/%Y")
        crud.create_todo_list(db, schemas.TodoListCreate(list_name="first list", date=date), 1)


# create tasklist everyday
@repeat_every(seconds=86400)
async def create_tasklist():
    db = SessionLocal()
    date = datetime.datetime.now().strftime("%d/%m/%Y")
    crud.create_todo_list(db, schemas.TodoListCreate(list_name="first list", date=date), 1)

# %USERPROFILE%/Documents/WORK/venvs/fastapi_venv/Scripts/activate.bat
# uvicorn todoApp.main:app --reload
# https://fastapi.tiangolo.com/tutorial/security/first-steps/
# https://github.com/borys25ol/fastapi-todo-example-app