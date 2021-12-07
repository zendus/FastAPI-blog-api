from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import user

# from . import models
# from .database import engine
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def index():
    return {"message": "Welcome to the new dispensation"}

app.include_router(user.router)