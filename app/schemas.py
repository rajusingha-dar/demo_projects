from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Pydantic models are used for data validation and serialization.
# They define the "shape" of the data your API will accept and return.

# --- Base Schema ---
# This is a base model that contains the common fields shared by
# both creating and reading a to-do item.
class TodoBase(BaseModel):
    """
    Base schema for a Todo item. Contains fields that are common
    for both creation and reading.
    """
    title: str
    description: Optional[str] = None # This field is optional
    completed: bool = False # Default value is False


# --- Schema for Creation ---
# This model is used when a user sends a request to create a new to-do.
# It inherits all fields from TodoBase. We don't want the user to specify
# an ID or creation timestamps, so we only include the base fields.
class TodoCreate(TodoBase):
    """
    Schema for creating a new Todo item. Inherits from TodoBase.
    This is what the user sends in a POST request body.
    """
    pass # It has the same fields as TodoBase, so no extra fields are needed.


# --- Schema for Reading/Returning ---
# This model is used when returning a to-do item from the API to the user.
# It includes the fields from the database that should be visible to the client,
# like 'id' and the timestamps.
class Todo(TodoBase):
    """
    Schema for reading a Todo item from the database. This is what will be
    returned in the API response. It includes database-generated fields.
    """
    id: int
    created_at: datetime
    updated_at: datetime

    # The Config class is used to provide configurations to Pydantic.
    # `orm_mode = True` tells the Pydantic model to read the data even if it
    # is not a dict, but an ORM model (like our SQLAlchemy 'Todo' model).
    # This allows the Pydantic model to be created directly from a database object.
    class Config:
        orm_mode = True
