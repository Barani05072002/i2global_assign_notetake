from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
import uuid

router = APIRouter(prefix="/notes", tags=["Notes"])

@router.post("/", response_model=schemas.NoteResponse)
def create_note(note: schemas.NoteCreate, user_id: uuid.UUID, db: Session = Depends(get_db)):
    db_note = models.Note(**note.model_dump(), user_id=user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.get("/", response_model=list[schemas.NoteResponse])
def get_notes(db: Session = Depends(get_db)):
    return db.query(models.Note).all()

@router.get("/{note_id}", response_model=schemas.NoteResponse)
def get_note(note_id: uuid.UUID, db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.note_id == str(note_id)).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note

@router.put("/{note_id}", response_model=schemas.NoteResponse)
def update_note(note_id: uuid.UUID, note: schemas.NoteCreate, db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.note_id == str(note_id)).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")

    for key, value in note.model_dump().items():
        setattr(db_note, key, value)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.delete("/{note_id}")
def delete_note(note_id: uuid.UUID, db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.note_id == str(note_id)).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(db_note)
    db.commit()
    return {"message": "Note deleted successfully"}
