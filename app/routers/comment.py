from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from .. import oauth2, models 
from ..database import get_db

from app import schemas

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db), 
current_user: int = Depends(oauth2.get_current_user)):
    new_comment = models.Comment(**comment.dict())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment