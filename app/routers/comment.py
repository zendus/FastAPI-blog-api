from fastapi import APIRouter, status, HTTPException, Response
from fastapi.params import Depends
from sqlalchemy.orm import Session
from .. import oauth2, models 
from ..database import get_db

from app import schemas

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db), 
current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == comment.post_id).first()
    if post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post with id: {comment.post_id} does not exist")
    comment.user_id = current_user.id
    new_comment = models.Comment(**comment.dict())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment


@router.put("/{id}", response_model=schemas.CommentResponse)
def update_comment(id: int, comment: schemas.CommentUpdate, db: Session = Depends(get_db),
current_user: int = Depends(oauth2.get_current_user)):
    target_comment_query = db.query(models.Comment).filter(models.Comment.id == id)
    target_comment = target_comment_query.first()
    if target_comment is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Comment with id: {id} does not exist")
    if target_comment.user_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

    target_comment_query.update(comment.dict(), synchronize_session=False)
    db.commit()
    db.refresh(target_comment)

    return target_comment


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(id: int, db: Session = Depends(get_db), 
current_user: int = Depends(oauth2.get_current_user)):
    target_comment_query = db.query(models.Comment).filter(models.Comment.id == id)
    comment = target_comment_query.first()
    if comment is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Comment with id: {id} does not exist.")
    if comment.user_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    target_comment_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)