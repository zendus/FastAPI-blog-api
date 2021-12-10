from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import cloudinary


cloudinary.config(
    cloud_name = settings.CLOUD_NAME,
    api_key = settings.CLOUDINARY_API_KEY,
    api_secret = settings.CLOUDINARY_API_SECRET
)


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# db connection using psycopg
while True:
    try:
        conn = psycopg2.connect(host=settings.DATABASE_HOSTNAME, database=settings.DATABASE_NAME,
        user=settings.DATABASE_USERNAME, password=settings.DATABASE_PASSWORD, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection successful !!!")
        break
    except Exception as error:
        print("Error occured while tring to connect DB")
        print("Error: ", error)
        time.sleep(4)