from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from typing import List

# Import all the components we've created
from . import crud, models, schemas
from .database import engine, get_db

# This command tells SQLAlchemy to create all the tables defined in models.py
# based on the engine's connection. It will check if the tables exist first
# before creating, so it's safe to run every time the application starts.
models.Base.metadata.create_all(bind=engine)

# Initialize the FastAPI application
app = FastAPI(title="To-Do App with FastAPI and MySQL")

# Mount the 'static' directory to serve static files like CSS and JavaScript
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Initialize Jinja2 templates to render HTML
templates = Jinja2Templates(directory="app/templates")


# --- API Endpoints (for programmatic access, e.g., from a mobile app) ---

@app.post("/api/todos/", response_model=schemas.Todo, tags=["API"])
def create_todo_api(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    """Create a new to-do item."""
    return crud.create_todo(db=db, todo=todo)


@app.get("/api/todos/", response_model=List[schemas.Todo], tags=["API"])
def read_todos_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve all to-do items."""
    return crud.get_todos(db, skip=skip, limit=limit)


@app.get("/api/todos/{todo_id}", response_model=schemas.Todo, tags=["API"])
def read_todo_api(todo_id: int, db: Session = Depends(get_db)):
    """Retrieve a single to-do item by its ID."""
    db_todo = crud.get_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


# --- HTML Endpoints (for the browser-based user interface) ---

@app.get("/", response_class=HTMLResponse, tags=["UI"])
def root(request: Request, db: Session = Depends(get_db)):
    """Renders the main HTML page with the list of all to-do items."""
    todos = crud.get_todos(db)
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})


@app.post("/add", response_class=RedirectResponse, tags=["UI"])
def add_todo_form(title: str = Form(...), description: str = Form(None), db: Session = Depends(get_db)):
    """Handles the form submission to create a new to-do item and redirects to the homepage."""
    todo_schema = schemas.TodoCreate(title=title, description=description)
    crud.create_todo(db=db, todo=todo_schema)
    return RedirectResponse(url="/", status_code=303) # 303 See Other is for redirecting after POST


@app.get("/toggle/{todo_id}", response_class=RedirectResponse, tags=["UI"])
def toggle_todo_form(todo_id: int, db: Session = Depends(get_db)):
    """Toggles the 'completed' status of a to-do item and redirects."""
    db_todo = crud.get_todo(db, todo_id)
    if db_todo:
        updated_data = schemas.TodoCreate(
            title=db_todo.title, 
            description=db_todo.description, 
            completed=not db_todo.completed
        )
        crud.update_todo(db, todo_id, updated_data)
    return RedirectResponse(url="/", status_code=303)


@app.get("/delete/{todo_id}", response_class=RedirectResponse, tags=["UI"])
def delete_todo_form(todo_id: int, db: Session = Depends(get_db)):
    """Deletes a to-do item and redirects."""
    crud.delete_todo(db, todo_id)
    return RedirectResponse(url="/", status_code=303)
