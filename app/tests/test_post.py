from .. import schemas

def test_get_all_posts(authorized_client, create_test_posts):
    response = authorized_client.get("/posts/")
    def validate(post):
        return schemas.PostResponse(**post)
    posts_map = map(validate, response.json())
    assert response.status_code == 200

def test_unauthorized_user_get_all_posts(client, create_test_posts):
    response = client.get("/posts/")
    assert response.status_code == 401

def test_unauthorized_user_get_one_post(client, create_test_posts):
    response = client.get(f"/posts/{create_test_posts[0].id}")
    assert response.status_code == 401