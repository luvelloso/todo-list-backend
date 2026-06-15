from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime, date
from typing import Optional
from models import TodoStatus, TodoCategory

# ==========================================
# SCHEMAS DE USUÁRIO
# ==========================================

class UserCreate(BaseModel):
    email: EmailStr = Field(..., max_length=100)
    full_name: str = Field(..., min_length=3, max_length=100)
    password: str

    @field_validator('password')
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError('A senha deve conter pelo menos 6 caracteres.')
        if not any(c.isupper() for c in v):
            raise ValueError('A senha deve conter pelo menos uma letra maiúscula.')
        if not any(c.isdigit() for c in v):
            raise ValueError('A senha deve conter pelo menos um número.')
        if not any(c in '!@#$%^&*()-_=+[]{}|;:\"\',.<>/?`~' for c in v):
            raise ValueError('A senha deve conter pelo menos um caractere especial.')
        return v

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    
    class Config:
        from_attributes = True


# ==========================================
# SCHEMAS DE TAREFA (TODO)
# ==========================================

class TodoBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: TodoStatus = TodoStatus.PENDING
    category: TodoCategory
    scheduled_date: date

class TodoCreate(TodoBase):
    pass

class TodoResponse(TodoBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    scheduled_date: date
    
    class Config:
        from_attributes = True

class TodoStatusUpdate(BaseModel):
    status: TodoStatus

# ==========================================
# SCHEMA DO TOKEN JWT
# ==========================================

class Token(BaseModel):
    access_token: str
    token_type: str
