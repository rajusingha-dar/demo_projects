from sqlalchemy.orm import Session
from . import models, schemas

# This file contains reusable functions to interact with the data in the database.

def get_todo(db: Session, todo_id: int):
    """
    Fetches a single to-do item from the database by its ID.
    
    Args:
        db (Session): The database session.
        todo_id (int): The ID of the to-do to retrieve.
        
    Returns:
        The Todo object if found, otherwise None.
    """
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()


def get_todos(db: Session, skip: int = 0, limit: int = 100):
    """
    Fetches a list of to-do items from the database.
    
    Args:
        db (Session): The database session.
        skip (int): The number of records to skip (for pagination).
        limit (int): The maximum number of records to return.
        
    Returns:
        A list of Todo objects.
    """
    return db.query(models.Todo).offset(skip).limit(limit).all()


def create_todo(db: Session, todo: schemas.TodoCreate):
    """
    Creates a new to-do item in the database.
    
    Args:
        db (Session): The database session.
        todo (schemas.TodoCreate): The Pydantic schema with the to-do data.
        
    Returns:
        The newly created Todo object.
    """
    # Create a new SQLAlchemy model instance from the Pydantic schema data
    db_todo = models.Todo(**todo.dict())
    db.add(db_todo)      # Add the new instance to the session
    db.commit()          # Commit the transaction to the database
    db.refresh(db_todo)  # Refresh the instance to get the new ID and defaults
    return db_todo


def update_todo(db: Session, todo_id: int, todo_data: schemas.TodoCreate):
    """
    Updates an existing to-do item in the database.
    
    Args:
        db (Session): The database session.
        todo_id (int): The ID of the to-do to update.
        todo_data (schemas.TodoCreate): The Pydantic schema with the updated data.
        
    Returns:
        The updated Todo object if found, otherwise None.
    """
    db_todo = get_todo(db, todo_id)
    if db_todo:
        update_data = todo_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_todo, key, value)
        db.commit()
        db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int):
    """
    Deletes a to-do item from the database.
    
    Args:
        db (Session): The database session.
        todo_id (int): The ID of the to-do to delete.
        
    Returns:
        The deleted Todo object if found, otherwise None.
    """
    db_todo = get_todo(db, todo_id)
    if db_todo:
        db.delete(db_todo)
        db.commit()
    return db_todo
