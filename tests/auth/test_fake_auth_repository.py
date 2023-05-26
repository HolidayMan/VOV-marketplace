import pytest

from auth.exceptions import UserDoesNotExist, UserAlreadyExists
from auth.repository import FakeUserRepository
from auth.models import UserInDB
from domain.user import UserRole, User


@pytest.fixture
def mock_user() -> UserInDB:
    return UserInDB(
        id=1,
        name="test",
        email="example@example.com",
        hashed_password="hashed_password",
        role=UserRole.CUSTOMER
    )


@pytest.fixture
def fake_auth_repository_with_mock_user(mock_user) -> FakeUserRepository:
    return FakeUserRepository(db={mock_user.id: mock_user})


def test_get_user(mock_user, fake_auth_repository_with_mock_user):
    user = mock_user
    repository = fake_auth_repository_with_mock_user

    # test get_user returns User
    result = repository.get_user(user.id)
    assert result == user.to_user()
    assert isinstance(result, User)

    # test get_user raises UserDoesNotExist if user does not exist
    with pytest.raises(UserDoesNotExist):
        repository.get_user(2304920)


def test_get_user_in_db_returns_user_if_user_exists(mock_user, fake_auth_repository_with_mock_user):
    user = mock_user
    repository = fake_auth_repository_with_mock_user

    result = repository.get_user_in_db(user.id)

    assert result == user
    assert isinstance(result, UserInDB)


def test_get_user_in_db_raises_user_does_not_exist_if_user_does_not_exist():
    repository = FakeUserRepository()

    with pytest.raises(UserDoesNotExist):
        repository.get_user_in_db(1)


def test_create_user():
    user = User(
        name="test",
        email="example@example.com",
        role=UserRole.CUSTOMER
    )
    repository = FakeUserRepository()

    # test create_user returns UserInDB with ID
    saved_user = repository.create_user(user, hashed_password="hashed_password")
    assert saved_user.id
    assert isinstance(saved_user, UserInDB)

    # test create_user adds user to db
    result = repository.get_user_in_db(saved_user.id)
    assert result == saved_user

    # test create_user raises UserAlreadyExists if user already exists
    with pytest.raises(UserAlreadyExists):
        repository.create_user(result, "hashed_password")

    # test create_user is immutable
    assert result is not user


def test_update_user(mock_user, fake_auth_repository_with_mock_user):
    user = mock_user
    repository = fake_auth_repository_with_mock_user

    # test update_user raises UserDoesNotExist if user does not exist
    with pytest.raises(UserDoesNotExist):
        repository.update_user(UserInDB(
            id=10000,
            name="test",
            email="example@example.com",
            role=UserRole.CUSTOMER,
            hashed_password="hashed_password",
        ))

    # test update_user returns UserInDB
    result = repository.update_user(user)
    assert isinstance(result, UserInDB)

    # test update_user updates user in db
    assert result == user
    assert repository.get_user_in_db(user.id) == user

    # test update_user raises UserDoesNotExist if user does not exist
    repository = FakeUserRepository()
    with pytest.raises(UserDoesNotExist):
        repository.update_user(user)


def test_delete_user(mock_user, fake_auth_repository_with_mock_user):
    user = mock_user
    repository = fake_auth_repository_with_mock_user

    # test delete_user deletes user from db
    repository.delete_user(user)
    with pytest.raises(UserDoesNotExist):
        repository.get_user_in_db(user.id)

    # test delete_user raises UserDoesNotExist if user does not exist
    with pytest.raises(UserDoesNotExist):
        repository.delete_user(user)


def test_exists(mock_user, fake_auth_repository_with_mock_user):
    user = mock_user
    repository = fake_auth_repository_with_mock_user

    # test exists returns True if user exists
    assert repository.exists(user.id)

    # test exists returns False if user does not exist
    assert not repository.exists(2304920)


def test_find_user(mock_user, fake_auth_repository_with_mock_user):
    user = mock_user
    repository = fake_auth_repository_with_mock_user

    # test find_user_by_email returns User if user exists
    result = repository.find_user(user.email, user.role)
    assert result == user.to_user()
    assert isinstance(result, User)


def test_find_user_returns_none_if_user_does_not_exist():
    repository = FakeUserRepository()

    assert repository.find_user("someemail@email.com", UserRole.CUSTOMER) is None


def test_find_user_in_db(mock_user, fake_auth_repository_with_mock_user):
    user = mock_user
    repository = fake_auth_repository_with_mock_user

    # test find_user_in_db_by_email returns UserInDB if user exists
    result = repository.find_user_in_db(user.email, UserRole.CUSTOMER)
    assert result == user
    assert isinstance(result, UserInDB)


def test_find_user_in_db_returns_none_if_user_does_not_exist():
    repository = FakeUserRepository()

    assert repository.find_user_in_db("someemail@email.com", UserRole.CUSTOMER) is None
