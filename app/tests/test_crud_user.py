def test_register_user(client):
    response = client.post("/auth/register", json={
        "username": "testusername",
        "first_name": "testfirstname",
        "last_name": "testlastname",
        "password": "testpassword"
    })
    assert response.status_code == 201
    assert response.json()["username"] == "testusername"


def test_login_user(client):
    client.post("/auth/register", json={
        "username": "testusername",
        "first_name": "testfirstname",
        "last_name": "testlastname",
        "password": "testpassword"
    })
    response = client.post("/auth/jwt/login", data={
        "username": "testuser@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_get_current_user(client):
    register_response = client.post("/auth/register", json={
        "username": "testusername",
        "first_name": "testfirstname",
        "last_name": "testlastname",
        "password": "testpassword"
    })
    assert register_response.status_code == 201
    login_response = client.post("/auth/jwt/login", data={
        "username": "testusername",
        "password": "testpassword"
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    response = client.get("/authenticated-only", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_reset_password(client):
    client.post("/auth/register", json={
        "username": "testusername",
        "first_name": "testfirstname",
        "last_name": "testlastname",
        "password": "testpassword"
    })
    response = client.post("/auth/forgot-password", json={"username": "testusername"})
    assert response.status_code == 202
