from pydantic import BaseModel
import re


EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
POSITIVE_INT_REGEX = r'\d+$'


class PositiveInt(int):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern=POSITIVE_INT_REGEX,
            examples=['1234', '1'],
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, int):
            raise TypeError('PositiveInt must be an integer!')
        if v < 1:
            raise ValueError('PositiveInt cannot be less than one!')
        return v


class Email(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern=EMAIL_REGEX,
            examples=['someone@somemail.com', 'email@example.com'],
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('Email must be string!')
        elif not re.fullmatch(EMAIL_REGEX, v):
            raise ValueError('Invalid email format!')
        else:
            return v
