import pytest
from pydantic import PositiveInt, EmailStr

from auth.logic import get_password_hash
from auth.models import UserInDB
from auth.repository import AsyncUserRepository, FakeUserRepository
from auth.services import process_user_login, process_create_user
from auth.exceptions import CredentialsInvalid, UserAlreadyExists
from domain.user import UserRole, User


@pytest.fixture
def mock_user() -> UserInDB:
    return UserInDB(
        id=1,
        name="test",
        email="example@example.com",
        hashed_password=get_password_hash("password"),
        role=UserRole.CUSTOMER
    )


@pytest.fixture
def repository_with_user(mock_user) -> AsyncUserRepository:
    return FakeUserRepository(db={mock_user.id: mock_user})


def test_process_user_login_returns_token_if_credentials_are_valid(repository_with_user):
    repository = repository_with_user
    user = repository.get_user_in_db(PositiveInt(1))
    result = process_user_login(repository, user.email, "password", user.role,)
    assert result is not None
    assert result.get("access_token") is not None


def test_process_user_login_raises_exception_if_credentials_are_invalid(repository_with_user):
    repository = repository_with_user
    user = repository.get_user_in_db(PositiveInt(1))
    with pytest.raises(CredentialsInvalid):
        process_user_login(repository, user.email, "wrong_password", user.role,)


def test_process_create_user_returns_access_token_if_user_created(repository_with_user):
    repository = repository_with_user
    user = User(name="test", email=EmailStr("newemail@email.com"), role=UserRole.CUSTOMER)

    result = process_create_user(repository, user, "password")
    assert result is not None
    assert result.get("access_token") is not None


def test_process_create_user_raises_exception_if_user_already_exists(repository_with_user):
    repository = repository_with_user
    user = repository.get_user_in_db(PositiveInt(1))
    with pytest.raises(UserAlreadyExists):
        process_create_user(repository, user, "password")
