from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app import schemas, oauth2
from .. import models
from ..database import get_db
from typing import List
from .. config import settings 
import os
ADMIN_Email = settings.ADMIN_Email
router = APIRouter(
    prefix="/files",
    tags=['Files'],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def upload_file(file: UploadFile = File(...), custom_filename: str = Form(None), db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    file_content = file.file.read()
    file_size = len(file_content)
    original_extension = os.path.splitext(file.filename)[1]
    if custom_filename:
        filename = f"{custom_filename}{original_extension}"
    else:
        filename = file.filename

    new_file = models.file_uploads(filename=filename, data=file_content, owner_id=current_user.id)
    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return {"details": f"file '{filename}' saved to database , size: {file_size} bytes"}


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
    
    if file.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    file_query.delete(synchronize_session=False)
    db.commit()
    return



@router.get("/download/{id}")
def download_file(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    file = db.query(models.file_uploads).filter(
        models.file_uploads.id == id).first()
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"file with id: {id} was not found")
    if current_user.email != ADMIN_Email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to download this file")
    return Response(
        content=file.data,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={file.filename}"}
    )