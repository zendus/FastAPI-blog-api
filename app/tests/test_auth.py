import pytest
from .. import schemas
from ..config import settings
from jose import jwt


@pytest.mark.parametrize("username, password, status_code", [
    ("johnnny@jh.com", "password123", 403),
    ("harry@gh.com", "password", 403)
])
def test_login_with_wrong_details(client, username, password, status_code):
    response = client.post("/login", data={"username": username, "password": password})
    assert response.status_code == status_code
    assert response.json()["detail"] == "Invalid Credentials"


@pytest.mark.parametrize("username, password, status_code", [
    (None, "password123", 422),
    ("johnnny@jh.com", None, 422)
])
def test_login_with_missing_details(client, username, password, status_code):
    response = client.post("/login", data={"username": username, "password": password})
    assert response.status_code == status_code
    assert response.json()["detail"][0]["msg"] == "field required"


def test_login(create_user, client):
    response = client.post("/login", data={"username": create_user["email"], "password": create_user["password"]})
    login_response = schemas.Token(**response.json())
    assert response.status_code == 200
    payload = jwt.decode(login_response.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    user_id = payload.get("user_id")
    assert user_id == create_user["id"]
    assert response.json()["token_type"] == "bearer"