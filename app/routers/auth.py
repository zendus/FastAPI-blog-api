from fastapi import status, HTTPException, Depends, Request
from fastapi.routing import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from pydantic.networks import EmailStr
from starlette.responses import Response

from app.routers.email import send_email
from .. import schemas, utils, models, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
import os


templates = Jinja2Templates(directory=os.path.abspath(os.path.expanduser("templates")))


router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User account yet to be verified")

    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/verify", response_class=HTMLResponse)
def verify_user(request: Request, token: str, db: Session = Depends(get_db)):
    email = utils.confirm_token(token)

    user_query = db.query(models.User).filter(models.User.email == email)
    user = user_query.first()
    if user and not user.is_active:
        user.is_active = True
        user_query.update(user.to_json(), synchronize_session=False)
        db.commit()
        return templates.TemplateResponse("verify.html", {"request": request, "user": user.username})
    else:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"Invalid Token", headers={"WWW-Authenticate": "Bearer"})  


@router.post("/re-verify")
async def reverify(request: schemas.ReverifyUser = Depends(schemas.ReverifyUser.as_form)):
    await send_email([request.email])
    return {"detail": "Email sent"}


