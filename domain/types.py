from pydantic import BaseModel


class ID(int):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, int):
            raise TypeError('Id must be an integer!')
        if v < 0:
            raise ValueError('Id cannot be less than zero!')
        return v
