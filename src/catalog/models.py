import datetime as dt
from dataclasses import dataclass

from src.catalog.errors import InvalidObjectError

MEDIA_OBJECT_FIELD_TYPES = {
    "id": str,
    "category": str,
    "name": str,
    "genre": str,
    "author": str,
    "duration": dt.timedelta,
    "size": int,
    "year": str
}

@dataclass
class MediaObject:
    id: str
    category: str
    name: str
    genre: str
    author: str
    duration: dt.timedelta
    size: int
    year: str

    def __post_init__(self):
        for attr in vars(self):
            field_type = MEDIA_OBJECT_FIELD_TYPES[attr]
            object_field_value = getattr(self, attr)
            if not isinstance(object_field_value, field_type):
                raise InvalidObjectError(
                    f"ERROR: Object field \"{attr}\" should have type {field_type}, not {type(object_field_value)}.\n"
                )
            if not object_field_value:
                raise InvalidObjectError(
                    "ERROR: Object field \"{attr}\" should have a valid value.\n"
                )

class MediaCatalog:
    pass
