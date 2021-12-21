from .. import schemas



def test_create_user(client):
    response = client.post("/users/", json={"username": "Harry213", "email": "harrystyles@england.com", 
    "password": "harrypassword"})
    new_user = schemas.UserResponse(**response.json())
    assert new_user.email == "harrystyles@england.com"
    assert response.status_code == 201