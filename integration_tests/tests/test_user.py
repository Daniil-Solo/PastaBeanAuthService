from fastapi import status
from httpx import AsyncClient
from src.dto.user import UserLoginDTO
from integration_tests.constants import USER_EMAIL, USER_PASSWORD
from integration_tests.urls import GET_USER_URL, LOGIN_URL, CHANGE_NAME_URL, CHANGE_EMAIL_URL, CHANGE_PASSWORD_URL


async def test_change_name(async_client: AsyncClient, register_one_user):
    new_name = "Antonios"
    # Login with right data
    response = await async_client.post(
        url=LOGIN_URL,
        json=UserLoginDTO(email=USER_EMAIL, password=USER_PASSWORD).model_dump()
    )
    auth_token = response.json()["auth_token"]
    assert response.status_code == status.HTTP_200_OK
    # Change name
    change_response = await async_client.post(
        url=CHANGE_NAME_URL,
        json={"new_name": new_name},
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )
    assert change_response.status_code == status.HTTP_200_OK
    # Getting user
    user_response = await async_client.get(
        url=GET_USER_URL,
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )
    assert user_response.status_code == status.HTTP_200_OK
    assert user_response.json()["name"] == new_name


async def test_change_email(async_client: AsyncClient, register_one_user):
    new_email = "tonios@mail.ru"
    # Login with right data
    response = await async_client.post(
        url=LOGIN_URL,
        json=UserLoginDTO(email=USER_EMAIL, password=USER_PASSWORD).model_dump()
    )
    auth_token = response.json()["auth_token"]
    assert response.status_code == status.HTTP_200_OK
    # Change email
    change_response = await async_client.post(
        url=CHANGE_EMAIL_URL,
        json={"new_email": new_email},
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )
    assert change_response.status_code == status.HTTP_200_OK
    # Getting user
    user_response = await async_client.get(
        url=GET_USER_URL,
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )
    assert user_response.status_code == status.HTTP_200_OK
    assert user_response.json()["email"] == new_email


async def test_change_password(async_client: AsyncClient, register_one_user):
    new_password = "Anton0000"
    # Login with right data
    response = await async_client.post(
        url=LOGIN_URL,
        json=UserLoginDTO(email=USER_EMAIL, password=USER_PASSWORD).model_dump()
    )
    auth_token = response.json()["auth_token"]
    assert response.status_code == status.HTTP_200_OK
    # Getting user
    user_response = await async_client.get(
        url=GET_USER_URL,
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )
    assert user_response.status_code == status.HTTP_200_OK
    last_password_update_date = user_response.json()["password_updated_at"]
    # Change password
    change_response = await async_client.post(
        url=CHANGE_PASSWORD_URL,
        json={"new_password": new_password},
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )
    assert change_response.status_code == status.HTTP_200_OK
    # Getting user
    user_response = await async_client.get(
        url=GET_USER_URL,
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )
    assert user_response.status_code == status.HTTP_200_OK
    assert user_response.json()["password_updated_at"] > last_password_update_date
    # Login with old password
    response = await async_client.post(
        url=LOGIN_URL,
        json=UserLoginDTO(email=USER_EMAIL, password=USER_PASSWORD).model_dump()
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
