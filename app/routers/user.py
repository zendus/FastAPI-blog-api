from fastapi import Response, status, HTTPException, Depends
from fastapi.routing import APIRouter
from ..database import get_db
from .. import schemas, utils, models, oauth2
from sqlalchemy.orm import Session
from . import email

router = APIRouter(
    tags=["Users"],
    prefix="/users"
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_email = db.query(models.User).filter(models.User.email == user.email).first()
    existing_username = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_username:    
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"User with username: {user.username} already exists.")
    if existing_email:    
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"User with email: {user.email} already exists.")
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    await email.send_email([user.email])
    return new_user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db), 
current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"User with id: {id} does not exist.")
    if id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

    return user


@router.put("/{id}", response_model=schemas.UserResponse)
def update_user(id: int, user: schemas.UserCreate, db: Session = Depends(get_db), 
current_user: int = Depends(oauth2.get_current_user)):
    target_user_query = db.query(models.User).filter(models.User.id == id)
    target_user = target_user_query.first()
    if target_user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"User with id: {id} does not exist")
    if id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    user.password = utils.hash(user.password)
    target_user_query.update(user.dict(), synchronize_session=False)
    db.commit()
    db.refresh(target_user)

    return target_user


@router.delete("/{id}")
def delete_user(id: int, db: Session = Depends(get_db), 
current_user: int = Depends(oauth2.get_current_user)):
    target_user_query = db.query(models.User).filter(models.User.id == id)
    user = target_user_query.first()
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"User with id: {id} does not exist.")
    if id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    target_user_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

    