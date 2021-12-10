from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Form, APIRouter
from starlette.responses import JSONResponse
from starlette.requests import Request
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from ..config import settings
from ..schemas import EmailSchema 
from .. import utils


conf = ConnectionConfig(
    MAIL_USERNAME = settings.MAIL_USERNAME,
    MAIL_PASSWORD = settings.MAIL_PASSWORD,
    MAIL_FROM = settings.MAIL_FROM,
    MAIL_PORT = settings.MAIL_PORT,
    MAIL_SERVER = settings.MAIL_SERVER,
    MAIL_TLS = settings.MAIL_TLS,
    MAIL_SSL = settings.MAIL_SSL
)

router = APIRouter(tags=["Email Authentication"])





@router.post("/email")
async def simple_send(email: EmailSchema) -> JSONResponse:

    print(email.dict().get("email")[0])
    confirmation_token = utils.generate_confirmation_token(email.dict().get("email")[0])
    html = f"""
<!DOCTYPE html>
<html>
<head>
</head>
<body>
    <div>
        <h3> Account Verification </h3>
        <br>
        <p>Welcome to the best blog on the planet, please 
        click on the link below to verify your account</p> 
        <br>
        <a style=" padding: 1rem; border-radius: 0.5rem; font-size: 1rem; 
        text-decoration: none; background: #0275d8; color: white;" 
        href="http://localhost:5000/verify?token={confirmation_token}">
            Verify your email
        <a>
       
    </div>
</body>
</html>

            """

    message = MessageSchema(
        subject="Best Blog Account Verification Email",
        recipients=email.dict().get("email"),  # List of recipients, as many as you can pass 
        body=html,
        subtype="html"
        )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})  