from typing import Annotated

from fastapi import Header

# X-Token: asdlkjflkewjaw49jeioewjfjewija


def fake_verify_customer(x_token: Annotated[str, Header()]):
    return True


def fake_verify_seller(x_token: Annotated[str, Header()]):
    return True


def fake_verify_moderator(x_token: Annotated[str, Header()]):
    return True
