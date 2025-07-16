from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from . import models, schemas

def get_todo(db: Session, todo_id: int):
    try:
        return db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    except SQLAlchemyError as e:
        print(f"Database error in get_todo: {e}")
        # Re-raise the exception to be handled by the API layer
        raise

def get_todos(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(models.Todo).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        print(f"Database error in get_todos: {e}")
        raise

def create_todo(db: Session, todo: schemas.TodoCreate):
    try:
        db_todo = models.Todo(**todo.dict())
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo
    except SQLAlchemyError as e:
        print(f"Database error in create_todo: {e}")
        # Rollback the transaction in case of error
        db.rollback()
        raise

def update_todo(db: Session, todo_id: int, todo_data: schemas.TodoCreate):
    try:
        db_todo = get_todo(db, todo_id)
        if db_todo:
            update_data = todo_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_todo, key, value)
            db.commit()
            db.refresh(db_todo)
        return db_todo
    except SQLAlchemyError as e:
        print(f"Database error in update_todo: {e}")
        db.rollback()
        raise

def delete_todo(db: Session, todo_id: int):
    try:
        db_todo = get_todo(db, todo_id)
        if db_todo:
            db.delete(db_todo)
            db.commit()
        return db_todo
    except SQLAlchemyError as e:
        print(f"Database error in delete_todo: {e}")
        db.rollback()
        raise
