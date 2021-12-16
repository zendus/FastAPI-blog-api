# FastAPI-blog-api

A blog API built using FastAPI framework with features like vote post (like, unlike), comment on a post, upload image along with post (Cloudinary), etc.



## How to Install

1. Clone the project in your local computer.

2. Create a virtualenv file.

3. Terminal/CLI command: <code>pip install --upgrade pip</code> to update your pip version.

4. Install all dependencies with <code>pip install -r requirements.txt</code>

5. Run <code>uvicorn app.main:app</code> to start the server.

## Main Dependencies

[FastAPI](https://fastapi.tiangolo.com "fastAPI") for api server<br>
[Uvicorn](https://www.uvicorn.org/ "uvicorn") - lightweight ASGI server<br>
[Pydantic](https://pydantic-docs.helpmanual.io/ "pydantic docs") to create schemas (comes with FastAPI by default)<br>
[Swagger UI](https://swagger.io/ "swagger ui website") for API documentation (embedded in FastAPI by default)<br>
[Redocs](https://redoc.ly/ "Redocly website") - alternative API documentation (embedded in FastAPI by default)<br>
[SQLAlchemy](https://www.sqlalchemy.org/ "SQLAlchemy") - database orm for interacting with SQL database<br>
[Bcrypt](https://pypi.org/project/bcrypt/ "bcrypt") - for password hashing<br>
[ItsDangerous](https://itsdangerous.palletsprojects.com/en/2.0.x/ "itsdangerous documentation") - for generating jwt tokens used for user authentication <br>
[Fastapi-Mail](https://sabuhish.github.io/fastapi-mail/ "fastapi-mail github documentation") - for sending verification mail to new user <br>
[Cloudinary](https://pypi.org/project/cloudinary/ "cloudinary pypi") - for post image upload <br>
[Psycopg2](https://www.psycopg.org/docs/ "psycopg2 documentation") - for postgreSQL database integration <br>


## Documentation 

[Click here to view swagger documentation](https://fastapi-blog-zendus.herokuapp.com/docs "hosted on heroku")<br> 