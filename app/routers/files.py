from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from app import schemas, oauth2
from .. import models
from ..database import get_db
from typing import List
import shutil
import os
router = APIRouter(
    prefix="/files",
    tags=['Files'],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def upload_file(file: UploadFile = File(...), custom_filename: str = Form(None), db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    file_content = file.file.read()

    filename = custom_filename if custom_filename else file.filename

    new_file = models.file_uploads(filename=filename, data=file_content, owner_id=current_user.id)
    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return {"details": f"file '{filename}' saved to database"}


@router.get("/", response_model=List[schemas.FileUploadOut])
def get_files(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    files = db.query(models.file_uploads).all()
    return files


@router.get("/{id}", response_model=schemas.FileUploadOut)
def get_file(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    file = db.query(models.file_uploads).filter(
        models.file_uploads.id == id).first()
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"file with id: {id} was not found")
    return file


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    file_query = db.query(models.file_uploads).filter(
        models.file_uploads.id == id)
    file = file_query.first()
    if file == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"file with id: {id} does not exist")
    file_query.delete(synchronize_session=False)
    db.commit()
    return
