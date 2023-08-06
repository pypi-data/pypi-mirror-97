import os
from googleplaces import GooglePlaces, Place
from magicdb import FrontendParserModel, magic_async, get_futures
from pydantic import BaseModel

google_places = GooglePlaces(os.getenv("GOOGLE_PLACES_API_KEY"))


class GoogleReview(FrontendParserModel):
    author_name: str = None
    author_url: str = None
    language: str = None
    profile_photo_url: str = None
    rating: int = None
    relative_time_description: str = None
    text: str = None
    time: int = None


def get_place(place_id) -> Place:
    place = google_places.get_place(place_id=place_id)
    return place


@magic_async
def try_get_photo(photo, max_h_w: int = 1000):
    times = 0
    while times < 3 and getattr(photo, "url", None) is None:
        try:
            photo.get(maxheight=max_h_w, maxwidth=max_h_w)
        except Exception as e:
            print("Places Error:", e)
            print("Trying again. Times:", times)
            times += 1


def download_images(place):
    get_futures([try_get_photo(photo=photo, future=True) for photo in place.photos])


def get_image_urls(place):
    download_images(place)
    return [photo.url for photo in place.photos if getattr(photo, "url", None)]


class Address(BaseModel):
    street_address: str = None
    city: str = None
    state_abbr: str = None
    postal_code: str = None
    country_name: str = None


def get_address_from_place(place: Place):
    add = place.details.get("adr_address")
    if not add:
        return
    chunks = add.split('<span class="')
    d = {}
    for chunk in chunks:
        if not chunk:
            continue
        try:
            label = chunk[: chunk.index('"')]
            value = chunk[chunk.index(">") + 1 : chunk.index("<")]
            d[label] = value
        except ValueError as e:
            print(f"Error With Location {e=}, {chunk=}")
    return Address(
        street_address=d.get("street-address"),
        city=d.get("locality"),
        state_abbr=d.get("region"),
        postal_code=d.get("postal-code"),
        country_name=d.get("country-name"),
    )
