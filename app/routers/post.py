from fastapi import Response, status, HTTPException, UploadFile, File
from fastapi.params import Depends
from fastapi import APIRouter
from .. import schemas, utils
import cloudinary
import cloudinary.uploader

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(file: UploadFile = File(...), post: schemas.PostCreate = Depends(schemas.PostCreate.as_form)):
    post_image = cloudinary.uploader.upload(file.file)
    url = post_image.get("url")
    print(post.title)
    return url
