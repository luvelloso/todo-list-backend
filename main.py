from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

import models
import schemas
import auth
import database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="To-Do List API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# ROTAS DE AUTENTICAÇÃO E USUÁRIO
# ==========================================

@app.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Este e-mail já está cadastrado.")
    
    hashed_pwd = auth.get_password_hash(user.password)
    new_user = models.User(email=user.email, full_name=user.full_name, hashed_password=hashed_pwd)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.UserResponse)
def get_me(current_user: models.User = Depends(auth.get_current_user)):
    """Retorna os dados do usuário logado (Essencial para o Frontend manter a sessão)"""
    return current_user


# ==========================================
# ROTAS DE TAREFAS (TO-DO)
# ==========================================

@app.post("/todos", response_model=schemas.TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo: schemas.TodoCreate, 
    current_user: models.User = Depends(auth.get_current_user), 
    db: Session = Depends(database.get_db)
):
    db_todo = models.Todo(
        title=todo.title,
        description=todo.description,
        category=todo.category,
        status=todo.status,
        scheduled_date=todo.scheduled_date,
        owner_id=current_user.id
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.get("/todos", response_model=List[schemas.TodoResponse])
def list_todos(
    status: Optional[models.TodoStatus] = None,
    scheduled_date: Optional[date] = None,
    current_user: models.User = Depends(auth.get_current_user), 
    db: Session = Depends(database.get_db)
):
    query = db.query(models.Todo).filter(models.Todo.owner_id == current_user.id)

    if status:
        query = query.filter(models.Todo.status == status)

    if scheduled_date:
        query = query.filter(models.Todo.scheduled_date == scheduled_date)

    return query.all()

@app.get("/todos/{todo_id}", response_model=schemas.TodoResponse)
def get_todo_by_id(
    todo_id: int, 
    current_user: models.User = Depends(auth.get_current_user), 
    db: Session = Depends(database.get_db)
):
    """Busca uma tarefa específica por ID garantindo a segurança do dono"""
    db_todo = db.query(models.Todo).filter(
        models.Todo.id == todo_id, 
        models.Todo.owner_id == current_user.id
    ).first()
    
    if not db_todo:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada ou não autorizada.")
        
    return db_todo

@app.put("/todos/{todo_id}/status", response_model=schemas.TodoResponse)
def update_todo_status(
    todo_id: int,
    status_update: schemas.TodoStatusUpdate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    """Atualização parcial: Altera apenas o status de forma rápida (Otimiza cliques no Frontend)"""
    db_todo = db.query(models.Todo).filter(
        models.Todo.id == todo_id, 
        models.Todo.owner_id == current_user.id
    ).first()
    
    if not db_todo:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada ou não autorizada.")
    
    db_todo.status = status_update.status
    
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: int, 
    current_user: models.User = Depends(auth.get_current_user), 
    db: Session = Depends(database.get_db)
):
    db_todo = db.query(models.Todo).filter(
        models.Todo.id == todo_id, 
        models.Todo.owner_id == current_user.id
    ).first()
    
    if not db_todo:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada ou não autorizada.")
    
    db.delete(db_todo)
    db.commit()
    return None
