import re

REGEX_PAT = "[A-Z]{4}[0-9]{5}"


class Code(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        # __modify_schema__ should mutate the dict it receives in place,
        # the returned value will be ignored
        field_schema.update(
            pattern=REGEX_PAT,
            examples=["COMP20007"],
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("string required")
        m = re.fullmatch(REGEX_PAT, v.upper())
        if m is None:
            raise ValueError("invalid code format")
        return cls(f"{m.group(0)}")

    def __repr__(self):
        return f"{super().__repr__()}"
