import pytest
from ..database import Base, get_db
from .database import engine, TestingSessionLocal
from starlette.testclient import TestClient
from ..main import app
from .. import oauth2

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def create_user(client):
    response = client.post("/users/", json={"username": "Harry213", "email": "harrystyles@england.com", 
    "password": "harrypassword"})
    new_user = response.json()
    new_user["password"] = "harrypassword"
    return new_user


@pytest.fixture
def create_access_token(create_user):
    return oauth2.create_access_token({"user_id": create_user["id"]})


@pytest.fixture
def authorized_client(client, create_access_token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {create_access_token}"
    }
    return client