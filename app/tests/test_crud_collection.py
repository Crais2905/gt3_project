import pytest
import pytest_asyncio


@pytest.fixture
def authorized_client(client):
    response = client.post(
        '/auth/register/',
        json={
            "email": "testuser@example.com",
            "password": "testpassword",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "username": "testuser",
            "first_name": "string",
            "last_name": "string"
        }
    )
    assert response.status_code == 200

    response = client.post(
        '/auth/login/',
        data={
            'username':  'testuser',
            'password': 'testpassword'
        }
    )
    assert response.status_code == 200
    access_token = response.json()['access_token']

    client.headers.update({'Authorization': f'Bearer {access_token}'})
    return client


# @pytest.fixture
# def authorized_client(client):
#     response = client.post(
#         '/auth/register/',
#         json={
#             "email": "testuser@example.com",
#             "password": "testpassword",
#             "is_active": True,
#             "is_superuser": False,
#             "is_verified": False,
#             "username": "testuser",
#             "first_name": "string",
#             "last_name": "string"
#         }
#     )
#     assert response.status_code == 200

#     response = client.post(
#         '/auth/login/',
#         data={
#             'username':  'testuser',
#             'password': 'testpassword'
#         }
#     )
#     assert response.status_code == 200
#     access_token = response.json()['access_token']

#     client.headers.update({'Authorization': f'Bearer {access_token}'})
#     yield client


# def test_create_get_collection(authorized_client):
#     response = authorized_client.post(
#         '/collections/',
#         json={
#             'title': 'test title'
#         }
#     )

#     assert response.status_code == 200

def test_get_collection_bad_id(client):
    response = client.get('/collections/1')
    assert response.status_code == 404