from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from . import crud, models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="To-Do App with FastAPI and MySQL")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# --- API Endpoints ---

@app.post("/api/todos/", response_model=schemas.Todo, tags=["API"])
def create_todo_api(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_todo(db=db, todo=todo)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

@app.get("/api/todos/", response_model=List[schemas.Todo], tags=["API"])
def read_todos_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        return crud.get_todos(db, skip=skip, limit=limit)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

@app.get("/api/todos/{todo_id}", response_model=schemas.Todo, tags=["API"])
def read_todo_api(todo_id: int, db: Session = Depends(get_db)):
    try:
        db_todo = crud.get_todo(db, todo_id=todo_id)
        if db_todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        return db_todo
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

# --- HTML Endpoints ---

@app.get("/", response_class=HTMLResponse, tags=["UI"])
def root(request: Request, db: Session = Depends(get_db)):
    try:
        todos = crud.get_todos(db)
        return templates.TemplateResponse("index.html", {"request": request, "todos": todos})
    except SQLAlchemyError as e:
        # You could render an error page here instead
        return templates.TemplateResponse("index.html", {"request": request, "todos": [], "error": f"Database error: {e}"})

@app.post("/add", response_class=RedirectResponse, tags=["UI"])
def add_todo_form(title: str = Form(...), description: str = Form(None), db: Session = Depends(get_db)):
    try:
        todo_schema = schemas.TodoCreate(title=title, description=description)
        crud.create_todo(db=db, todo=todo_schema)
        return RedirectResponse(url="/", status_code=303)
    except SQLAlchemyError:
        # In a real app, you might redirect to an error page with a message
        return RedirectResponse(url="/?error=true", status_code=303)

@app.get("/toggle/{todo_id}", response_class=RedirectResponse, tags=["UI"])
def toggle_todo_form(todo_id: int, db: Session = Depends(get_db)):
    try:
        db_todo = crud.get_todo(db, todo_id)
        if db_todo:
            updated_data = schemas.TodoCreate(
                title=db_todo.title, 
                description=db_todo.description, 
                completed=not db_todo.completed
            )
            crud.update_todo(db, todo_id, updated_data)
        return RedirectResponse(url="/", status_code=303)
    except SQLAlchemyError:
        return RedirectResponse(url="/?error=true", status_code=303)

@app.get("/delete/{todo_id}", response_class=RedirectResponse, tags=["UI"])
def delete_todo_form(todo_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_todo(db, todo_id)
        return RedirectResponse(url="/", status_code=303)
    except SQLAlchemyError:
        return RedirectResponse(url="/?error=true", status_code=303)
