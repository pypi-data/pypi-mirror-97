from typing import ClassVar
from pydantic import BaseModel, validator
from slugify import slugify as base_slugify


class SlugModelSpeed(BaseModel):
    """ Adds slug and helper slug methods to MagicModel. Must use this with MagicModel """

    _slugify_kwargs: ClassVar[dict] = {"separator": "", "replacements": [["&", "and"]]}
    slug: str

    @classmethod
    def slugify(cls, slug):
        return base_slugify(slug, **cls._slugify_kwargs)

    @classmethod
    def create_slug(cls, value_to_slugify: str):
        slug_base = cls.slugify(value_to_slugify)
        slug = slug_base
        number = 1
        while cls.get_by_slug(slug):
            slug = cls.slugify(f"{slug_base}{number}")
            number += 1
        return slug

    @classmethod
    def get_by_slug(cls, slug):
        models = cls.collection.where("slug", "==", slug).stream()
        return None if not models else models[0]

    def unique_slug(self, slug):
        models = self.get_by_slug(slug)
        for model in models:
            if model.id != self.id:
                return False
        return True


class SlugModel(SlugModelSpeed):
    @validator("slug")
    def parse_slug(cls, v):
        return cls.slugify(v)
