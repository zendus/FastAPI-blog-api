from .. import schemas

def test_login_with_non_existing_user(client):
    response = client.post("/login", data={"username": "johndoe@john.com", "password": "password123"})
    # login_response = schemas.Token(**response.json())
    print(response.json())
    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid Credentials"


def test_login(client, create_user):
    response = client.post("/login", data={"username": create_user["email"], "password": create_user["password"]})
    login_response = schemas.Token(**response.json())
    assert response.status_code == 200