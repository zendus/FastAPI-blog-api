from fastapi import Response, status, HTTPException
from fastapi.routing import APIRouter
from ..database import cursor, conn
from .. import schemas, utils

router = APIRouter(
    tags=["Users"],
    prefix="/users"
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate):
    hashed_password = utils.hash(user.password)
    try:
        cursor.execute(""" INSERT INTO users (username, email, password) VALUES (%s, %s, %s) 
        RETURNING id, username, email, created_at, is_active """, (user.username, user.email, hashed_password))
        new_user = cursor.fetchone()
        conn.commit()
        return new_user
    except Exception as e:
        error = str(e).replace("\n", " ").replace("\"", " * ")
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"{error}")



@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
def get_user_by_id(id: int):
    cursor.execute(""" SELECT * FROM users WHERE id = %s""", (id,))
    user = cursor.fetchone()
    if not user or user["is_active"] != True:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"User with id {id} not found")
    return user 