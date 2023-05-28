import pytest
from pydantic import EmailStr

from auth.logic import get_password_hash, get_user, authenticate_user, create_access_token, get_user_by_token, \
    create_user
from auth.models import UserInDB, UserTokenData
from auth.repository import FakeUserRepository, AsyncUserRepository
from auth.exceptions import UserAlreadyExists
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


def test_get_user(mock_user, repository_with_user):

    # test get_user returns User
    result = repository_with_user.get_user_in_db(mock_user.id)
    assert result == get_user(repository_with_user, mock_user.email, mock_user.role)


def test_get_user_returns_none_if_user_does_not_exist(repository_with_user):
    assert get_user(repository_with_user, EmailStr("someprettyemail@email.com"), UserRole.CUSTOMER) is None


def test_authenticate_user_returns_user_if_user_exists(mock_user, repository_with_user):
    user = mock_user
    repository = repository_with_user

    result = authenticate_user(repository, user.email, user.role, "password")

    assert result == user


def test_authenticate_user_returns_none_if_user_does_not_exist(repository_with_user):
    repository = repository_with_user

    result = authenticate_user(repository, EmailStr("someprettyemail@example.com"), UserRole.CUSTOMER, "password")
    assert result is None


def test_authenticate_user_returns_none_if_password_is_incorrect(mock_user, repository_with_user):
    user = mock_user
    repository = repository_with_user

    result = authenticate_user(repository, user.email, user.role, "wrong_password")
    assert result is None


def test_create_access_token_returns_token(mock_user):
    user = mock_user
    result = create_access_token(UserTokenData(sub=user.email, role=user.role))
    assert isinstance(result, str)


def test_get_user_by_token_returns_user_if_token_is_valid(mock_user, repository_with_user):
    user = mock_user
    token = create_access_token(UserTokenData(sub=user.email, role=user.role))
    result = get_user_by_token(repository_with_user, token)
    assert result == user


def test_create_user_returns_user_if_user_does_not_exist(repository_with_user):
    repository = repository_with_user
    user = User(
        name="test",
        email="email@email.com",
        role=UserRole.CUSTOMER
    )

    result = create_user(repository, user, "password")
    assert result == repository.get_user_in_db(result.id)


def test_create_user_raises_exception_if_user_exists(mock_user, repository_with_user):
    repository = repository_with_user
    user = mock_user.to_user()

    with pytest.raises(UserAlreadyExists):
        create_user(repository, user, "password")
