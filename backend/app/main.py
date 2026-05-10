from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import ai_service, models, schemas
from .auth import create_token, get_user_from_token, hash_password, verify_password
from .database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI-Powered CRM Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

def current_user(authorization: str | None = Header(default=None), db: Session = Depends(get_db)) -> models.User:
    user = get_user_from_token(db, authorization)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token")
    return user

@app.post("/auth/register", response_model=schemas.AuthResponse)
def register(payload: schemas.RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = models.User(email=payload.email, password_hash=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"token": create_token(user.id), "email": user.email}

@app.post("/auth/login", response_model=schemas.AuthResponse)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"token": create_token(user.id), "email": user.email}

@app.get("/clients", response_model=list[schemas.ClientOut])
def list_clients(user: models.User = Depends(current_user), db: Session = Depends(get_db)):
    return db.query(models.Client).filter(models.Client.owner_id == user.id).order_by(models.Client.id.desc()).all()

@app.post("/clients", response_model=schemas.ClientOut)
def create_client(payload: schemas.ClientCreate, user: models.User = Depends(current_user), db: Session = Depends(get_db)):
    client = models.Client(**payload.model_dump(), owner_id=user.id)
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

@app.put("/clients/{client_id}", response_model=schemas.ClientOut)
def update_client(client_id: int, payload: schemas.ClientUpdate, user: models.User = Depends(current_user), db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.id == client_id, models.Client.owner_id == user.id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(client, key, value)
    db.commit()
    db.refresh(client)
    return client

@app.delete("/clients/{client_id}")
def delete_client(client_id: int, user: models.User = Depends(current_user), db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.id == client_id, models.Client.owner_id == user.id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(client)
    db.commit()
    return {"deleted": True}

@app.get("/clients/{client_id}/notes", response_model=list[schemas.NoteOut])
def list_notes(client_id: int, user: models.User = Depends(current_user), db: Session = Depends(get_db)):
    _get_client_or_404(db, client_id, user.id)
    return db.query(models.Note).filter(models.Note.client_id == client_id).order_by(models.Note.created_at.desc()).all()

@app.post("/clients/{client_id}/notes", response_model=schemas.NoteOut)
def create_note(client_id: int, payload: schemas.NoteCreate, user: models.User = Depends(current_user), db: Session = Depends(get_db)):
    _get_client_or_404(db, client_id, user.id)
    note = models.Note(client_id=client_id, content=payload.content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

@app.post("/ai/client-summary/{client_id}", response_model=schemas.AIResponse)
def client_summary(client_id: int, user: models.User = Depends(current_user), db: Session = Depends(get_db)):
    client = _get_client_or_404(db, client_id, user.id)
    notes = db.query(models.Note).filter(models.Note.client_id == client_id).all()
    return {"result": ai_service.generate_summary(client, notes)}

@app.post("/ai/follow-up/{client_id}", response_model=schemas.AIResponse)
def follow_up(client_id: int, user: models.User = Depends(current_user), db: Session = Depends(get_db)):
    client = _get_client_or_404(db, client_id, user.id)
    notes = db.query(models.Note).filter(models.Note.client_id == client_id).all()
    return {"result": ai_service.generate_follow_up(client, notes)}

def _get_client_or_404(db: Session, client_id: int, owner_id: int) -> models.Client:
    client = db.query(models.Client).filter(models.Client.id == client_id, models.Client.owner_id == owner_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client
