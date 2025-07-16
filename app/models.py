from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base

# This is the SQLAlchemy ORM model for our 'todos' table.
# By inheriting from 'Base' (which we defined in database.py), SQLAlchemy's
# declarative system knows that this class corresponds to a database table.

class Todo(Base):
    """
    Represents a to-do item in the database.
    """
    # __tablename__ tells SQLAlchemy the name of the table to use in the database.
    __tablename__ = "todos"

    # Define the columns of the 'todos' table.
    # Each attribute of the class represents a column.

    # id: An integer column that is the primary key for the table.
    # `primary_key=True` makes this column the unique identifier for each row.
    # `index=True` creates a database index on this column, which speeds up queries.
    id = Column(Integer, primary_key=True, index=True)

    # title: A string column to hold the text of the to-do item.
    # `String(255)` limits the length of the title to 255 characters.
    # `nullable=False` means this column cannot be empty.
    # `index=True` is good for columns that are frequently used in 'WHERE' clauses.
    title = Column(String(255), nullable=False, index=True)

    # description: A string column for a more detailed description of the to-do.
    # It can be empty (`nullable=True`).
    description = Column(String(500), nullable=True)

    # completed: A boolean column to mark a to-do as done or not.
    # `server_default='0'` sets the default value in the database to False (0 for boolean).
    # `nullable=False` ensures every to-do has a completion status.
    completed = Column(Boolean, server_default='0', nullable=False)

    # created_at: A datetime column to store when the to-do was created.
    # `server_default=func.now()` tells the database to automatically set the
    # current timestamp when a new row is created.
    created_at = Column(DateTime, server_default=func.now())

    # updated_at: A datetime column to store the last update time.
    # `onupdate=func.now()` tells the database to automatically update this
    # timestamp whenever the row is modified.
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        """
        Provides a developer-friendly string representation of the Todo object,
        useful for debugging.
        """
        return f"<Todo(id={self.id}, title='{self.title}', completed={self.completed})>"