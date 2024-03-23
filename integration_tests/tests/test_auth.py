import pytest
from fastapi import status
from httpx import AsyncClient
from src.dto.user import UserRegisterDTO, UserLoginDTO, UserDTO
from src.endpoints.schemas import LoginResponse
from integration_tests.constants import USER_NAME, USER_EMAIL, USER_PASSWORD, OTHER_USER_NAME, OTHER_USER_EMAIL, \
    OTHER_USER_PASSWORD
from integration_tests.urls import REGISTER_URL, LOGIN_URL, LOGOUT_URL, GET_USER_URL


@pytest.mark.parametrize('password', ["", "1234567890", "bad password", "sma11"])
async def test_register_with_invalid_password(async_client: AsyncClient, password: str):
    invalid_password_response = await async_client.post(
        url=REGISTER_URL,
        json=UserRegisterDTO(name=USER_NAME, email=USER_EMAIL, password=password).model_dump()
    )
    assert invalid_password_response.status_code == status.HTTP_400_BAD_REQUEST


async def test_register(async_client: AsyncClient, register_one_user):
    # Existing name
    valid_response = await async_client.post(
        url=REGISTER_URL,
        json=UserRegisterDTO(name=USER_NAME, email=OTHER_USER_NAME, password=USER_PASSWORD).model_dump()
    )
    assert valid_response.status_code == status.HTTP_400_BAD_REQUEST
    # Existing email
    valid_response = await async_client.post(
        url=REGISTER_URL,
        json=UserRegisterDTO(name=OTHER_USER_NAME, email=USER_EMAIL, password=USER_PASSWORD).model_dump()
    )
    assert valid_response.status_code == status.HTTP_400_BAD_REQUEST


async def test_login(async_client: AsyncClient, register_one_user):
    # Login with wrong email
    response = await async_client.post(
        url=LOGIN_URL,
        json=UserLoginDTO(email=OTHER_USER_EMAIL, password=USER_PASSWORD).model_dump()
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    # Login with wrong password
    response = await async_client.post(
        url=LOGIN_URL,
        json=UserLoginDTO(email=USER_EMAIL, password=OTHER_USER_PASSWORD).model_dump()
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    # Login with right data
    response = await async_client.post(
        url=LOGIN_URL,
        json=UserLoginDTO(email=USER_EMAIL, password=USER_PASSWORD).model_dump()
    )
    auth_token = response.json()["auth_token"]
    assert response.status_code == status.HTTP_200_OK
    assert LoginResponse.model_validate(response.json())
    assert response.json()["name"] == USER_NAME
    assert response.json()["email"] == USER_EMAIL
    # Getting user with auth token
    response = await async_client.get(
        url=GET_USER_URL,
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert UserDTO.model_validate(response.json())
    assert response.json()["name"] == USER_NAME
    assert response.json()["email"] == USER_EMAIL


async def test_logout(async_client: AsyncClient):
    # Register new user
    response = await async_client.post(
        url=REGISTER_URL,
        json=UserRegisterDTO(name=USER_NAME, email=USER_EMAIL, password=USER_PASSWORD).model_dump()
    )
    assert response.status_code == status.HTTP_200_OK
    # Login
    response = await async_client.post(
        url=LOGIN_URL,
        json=UserLoginDTO(email=USER_EMAIL, password=USER_PASSWORD).model_dump()
    )
    auth_token = response.json()["auth_token"]
    assert response.status_code == status.HTTP_200_OK
    # Getting user
    response = await async_client.get(
        url=GET_USER_URL,
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    # Logout
    response = await async_client.post(
        url=LOGOUT_URL,
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    # Getting user again (expected no user)
    response = await async_client.get(
        url=GET_USER_URL,
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
