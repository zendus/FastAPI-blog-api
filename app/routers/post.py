from fastapi import Response, status, HTTPException
from fastapi.params import Depends
from fastapi import APIRouter
from ..database import cursor, conn
from .. import schemas, utils

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate = Depends(schemas.PostCreate.as_form)):
    return post
