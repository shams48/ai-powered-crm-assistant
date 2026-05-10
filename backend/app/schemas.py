from datetime import datetime
from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    token: str
    email: str

class ClientCreate(BaseModel):
    name: str
    company: str = ""
    email: str = ""
    status: str = "Lead"
    priority: str = "Medium"
    last_contact_date: str = ""

class ClientUpdate(BaseModel):
    name: str | None = None
    company: str | None = None
    email: str | None = None
    status: str | None = None
    priority: str | None = None
    last_contact_date: str | None = None

class ClientOut(ClientCreate):
    id: int

    class Config:
        from_attributes = True

class NoteCreate(BaseModel):
    content: str

class NoteOut(BaseModel):
    id: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class AIResponse(BaseModel):
    result: str
