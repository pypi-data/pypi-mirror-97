from __future__ import annotations
import requests
from magicdb import FrontendParserModel
from . import places
from datetime import datetime
import pytz
from typing import Optional

tz_from_coords_url = (
    "https://getzipcodeinfo.herokuapp.com/get_tz_from_coords?lat=<LAT>&lng=<LNG>"
)


def tz_from_coords(lat: float, lng: float):
    url = tz_from_coords_url.replace("<LAT>", str(lat)).replace("<LNG>", str(lng))
    return requests.get(url).json()


class Location(FrontendParserModel):
    lat: float
    lng: float
    city: str = None
    state_abbr: str = None
    country_id: int = None
    country_name: str = None
    postal_code: str = None

    street_address: str = None
    unit: str = None

    timezone: str
    place_id: str = None

    @classmethod
    def from_place(cls, place: places.Place) -> Location:
        parsed_address = places.get_address_from_place(place=place)
        print(f"{parsed_address=}")

        lat, lng = place.geo_location["lat"], place.geo_location["lng"]
        timezone = tz_from_coords(lat=lat, lng=lng)

        return Location(
            lat=lat,
            lng=lng,
            city=parsed_address.city,
            state_abbr=parsed_address.state_abbr,
            postal_code=parsed_address.postal_code,
            country_name=parsed_address.country_name,
            street_address=parsed_address.street_address,
            timezone=timezone,
            place_id=place.place_id,
        )

    @classmethod
    def from_place_id(cls, place_id: str) -> Location:
        place = places.get_place(place_id=place_id)
        return cls.from_place(place)

    def display_address(self):
        return f"{self.street_address}, {self.city}, {self.state_abbr} {self.postal_code}, {self.country_name}"

    def display_city_and_state(self):
        return f"{self.city}, {self.state_abbr}"

    def prettify_date(self, date: datetime) -> Optional[str]:
        """Takes in a date. If the date is not localized, localize it to UTC."""
        if not date:
            return None
        try:
            if not self.timezone:
                return None
            d = date if date.tzinfo else pytz.utc.localize(date)
            tz = pytz.timezone(self.timezone)
            tz_date = d.astimezone(tz)
            return tz_date.strftime("%b %d, %Y at %I:%M %p")
        except Exception as e:
            print(f"Error in prettify_data: {e=}")
            return None
