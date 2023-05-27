from domain.user import UserRole, User

EXAMPLE_EMAIL = "example@example.com"


def get_mock_user() -> User:
    return User(
        id=1,
        name="test",
        email=EXAMPLE_EMAIL,
        role=UserRole.CUSTOMER
    )


def test_user_equal_to_itself():
    user = get_mock_user()
    assert user == user


def test_user_equal_to_user_with_same_id_email_and_role():
    user = get_mock_user()

    assert user == User(
        id=1,
        name="test",
        email=EXAMPLE_EMAIL,
        role=UserRole.CUSTOMER
    )


def test_user_not_equal_to_user_with_different_id_email_or_role():
    user = get_mock_user()

    # test user is not equal to another user with different email
    assert user != User(
        id=1,
        name="test",
        email="anotheremail@example.com",
        role=UserRole.CUSTOMER
    )

    # test user is not equal to another user with different role
    assert user != User(
        id=1,
        name="test",
        email=EXAMPLE_EMAIL,
        role=UserRole.SELLER
    )


def test_user_not_equal_to_other_objects():
    user = get_mock_user()

    # test user is not equal to another object
    assert user != "not a user"


def test_user_not_equal_to_user_with_different_id():
    user = get_mock_user()

    # test user is not equal to another user with different id
    assert user != User(
        id=2,
        name="test",
        email=EXAMPLE_EMAIL,
        role=UserRole.CUSTOMER
    )


def test_user_hash():
    user = get_mock_user()

    # test user hash is equal to hash of user with same id, email, and role
    assert hash(user) == hash(User(
        id=1,
        name="test",
        email=EXAMPLE_EMAIL,
        role=UserRole.CUSTOMER
    ))

    # test user hash is not equal to hash of user with different id, email, or role
    assert hash(user) != hash(User(
        id=2,
        name="test",
        email=EXAMPLE_EMAIL,
        role=UserRole.CUSTOMER
    ))
    assert hash(user) != hash(User(
        id=1,
        name="test",
        email="test@test.com",
        role=UserRole.CUSTOMER
    ))

