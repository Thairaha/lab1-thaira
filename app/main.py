import os

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database import Base, engine, get_db
from app import models, schemas

APP_ENV = os.getenv("APP_ENV", "development")

app = FastAPI(title="team-notes-api")

# Crea las tablas si no existen (estrategia simple de inicializacion para el laboratorio)
Base.metadata.create_all(bind=engine)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # El laboratorio pide 400 Bad Request para datos invalidos; FastAPI usa 422 por
    # defecto, asi que lo homologamos aqui.
    return JSONResponse(status_code=400, content={"detail": "Invalid or missing data"})


@app.get("/health")
def health_check():
    return {"status": "ok", "environment": APP_ENV}


@app.get("/notes", response_model=list[schemas.NoteOut])
def list_notes(db: Session = Depends(get_db)):
    notes = db.query(models.Note).order_by(models.Note.id).all()
    return notes


@app.get("/notes/{note_id}", response_model=schemas.NoteOut)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.post("/notes", response_model=schemas.NoteOut, status_code=201)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    try:
        db_note = models.Note(title=note.title, content=note.content, author=note.author)
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        return db_note
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")


@app.put("/notes/{note_id}", response_model=schemas.NoteOut)
def update_note(note_id: int, note: schemas.NoteUpdate, db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    db_note.title = note.title
    db_note.content = note.content
    db_note.author = note.author

    try:
        db.commit()
        db.refresh(db_note)
        return db_note
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")


@app.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(db_note)
    db.commit()
    return {"detail": "Note deleted"}
