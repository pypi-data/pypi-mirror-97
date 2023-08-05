from datetime import datetime

from pydantic import Field

from magicdb.Models import MagicModelSpeed


class DateModelSpeed(MagicModelSpeed):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    def update(self, last_updated=None, *args, **kwargs):
        self.last_updated = last_updated or datetime.utcnow()
        return super().update(*args, **kwargs)
