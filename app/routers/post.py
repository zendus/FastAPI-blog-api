from fastapi import Response, status, HTTPException, UploadFile, File
from fastapi.params import Depends
from fastapi import APIRouter
from typing import List, Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session, load_only
from sqlalchemy.sql.functions import func
from .. import schemas, utils, models, oauth2
import cloudinary
import cloudinary.uploader
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(file: UploadFile = File(...), post: schemas.PostCreate = Depends(schemas.PostCreate.as_form), 
db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    try:
        post_image = cloudinary.uploader.upload(file.file)
        url = post_image.get("url")
        post.image_url = url
    except Exception as e:
        pass
    post.owner_id = current_user.id
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostWithComments)
def get_post_by_id(id: int, db: Session = Depends(get_db),
current_user: int = Depends(oauth2.get_current_user)):

    # post = db.query(models.Post, (db.query(models.Comment).filter(models.Comment.post_id == id).options(load_only("opinion"))).label("Comments")).join(
    #     models.Comment, models.Comment.post_id == models.Post.id, isouter=True
    # ).group_by(models.Post.id).filter(models.Post.id == id).first()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    comments = db.query(models.Comment).filter(models.Comment.post_id == id).all()

    if post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post with id: {id} does not exist.")

    return {"Post": post, "Comments": comments}


@router.get("/", response_model=List[schemas.PostResponse])
def get_all_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
limit: Optional[int] = 10, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(or_(models.Post.title.contains(search),
    models.Post.content.contains(search))).limit(limit).all()
    return posts


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, file: UploadFile = File(...), 
post: schemas.PostUpdate = Depends(schemas.PostUpdate.as_form), db: Session = Depends(get_db), 
current_user: int = Depends(oauth2.get_current_user)):
    target_post_query = db.query(models.Post).filter(models.Post.id == id)
    target_post = target_post_query.first()
    if target_post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post with id: {id} does not exist")
    if target_post.owner_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    if file:
        try:
            post_image = cloudinary.uploader.upload(file.file)
            url = post_image.get("url")
            post.image_url = url
        except Exception as e:
            pass
    else:
        post.image_url = None
    target_post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(target_post)

    return 
    

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), 
current_user: int = Depends(oauth2.get_current_user)):
    target_post_query = db.query(models.Post).filter(models.Post.id == id)
    post = target_post_query.first()
    if post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post with id: {id} does not exist.")
    if post.owner_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    target_post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)