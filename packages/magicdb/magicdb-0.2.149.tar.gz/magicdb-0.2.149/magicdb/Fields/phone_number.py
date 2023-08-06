import phonenumbers
from pydantic import BaseModel
import re


class PhoneNumber(str):
    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        # __modify_schema__ should mutate the dict it receives in place,
        # the returned value will be ignored
        field_schema.update(
            # some example phonenumbers
            examples=["609-356-9384", "+16093284938"],
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("string required")

        # two edge cases for american numbers-- all non american numbers must have a +<countrycode>
        # if there is no + and the len of all digits is 10 and there is no leading 1... add a +1
        #   if there len of all digits is 11 and there is a leading 1, add a +

        if "+" not in v:
            digits = "".join(re.findall(r"\d+", v))
            if len(digits) == 10 and digits[0] != "1":
                v = "+1" + v
            elif len(digits) == 11 and digits[0] == "1":
                v = "+" + v

        try:
            x = phonenumbers.parse(v)
            formatted = phonenumbers.format_number(
                x, phonenumbers.PhoneNumberFormat.E164
            )
            return cls(formatted)
        except phonenumbers.phonenumberutil.NumberParseException as err:
            raise ValueError(err, "given phone number value:", v)

    def __repr__(self):
        return f"PhoneNumber({super().__repr__()})"


if __name__ == "__main__":

    class Model(BaseModel):
        phone_number: PhoneNumber

    model = Model(phone_number="(4555)555-5555")
    print("model", model)
    print("model phone num", model.phone_number)
    print(type(model.phone_number))
