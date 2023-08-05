from pydantic import BaseModel, validator


class FrontendParserModel(BaseModel):
    """
    Model turns all optional empty strings to None, removes all
    empty string or None elements from an array, and strips whitespace.
    """

    @staticmethod
    def empty_str(v):
        return type(v) == str and v.strip() == ""

    @validator("*", pre=True)
    def empty_str_to_none(cls, v, field):
        if (
            cls.empty_str(v)
            and not field.required
            and getattr(field, "default", True) is None
        ):
            v = None
        return v

    @validator("*", pre=True)
    def remove_empty_string_and_nones_from_list(cls, v):
        if type(v) != list:
            return v
        new_v = []
        """If list -- only include valid values -- and strip strs"""
        for e in v:
            if e is None or cls.empty_str(e):
                continue
            if type(e) == str:
                e = e.strip()
            new_v.append(e)
        return new_v

    class Config:
        anystr_strip_whitespace = True
