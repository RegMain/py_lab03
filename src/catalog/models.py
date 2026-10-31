from dataclasses import dataclass

from catalog.errors import IDDuplicateError, InvalidObjectError, ObjectNotFoundError

MEDIA_OBJECT_FIELD_TYPES = {
    "id": str,
    "category": str,
    "name": str,
    "genre": str,
    "author": str,
    "duration": int,
    "size": int,
    "year": int
}

@dataclass
class MediaObject:
    id: str # Unique
    category: str
    name: str
    genre: str
    author: str
    duration: int # time in ms
    size: int # size in bytes
    year: int

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
    __data: dict[str, MediaObject]
    __categories: dict[str, list[str]]
    __names: dict[str, list[str]]

    def __init__(self):
        self.__data = {}
        self.__categories = {}
        self.__names = {}

    def __len__(self):
        return len(self.__data)

    def __iter__(self):
        return iter(self.__data)

    def __contains__(self, item_id: str):
        return item_id in self.__data

    def add(self, item: MediaObject) -> None:
        if not isinstance(item, MediaObject):
            raise InvalidObjectError(
                "ERROR: Trying to insert non MediaObject type object in catalog.\n"
            )
        if self.__contains__(item.id):
            raise IDDuplicateError(
                f"ERROR: Trying to insert object with existing id \"{item.id}\" in catalog.\n"
            )
        self.__data[item.id] = item
        if item.category.title() not in self.__categories:
            self.__categories[item.category.title()] = [item.id]
        else:
            self.__categories[item.category.title()].append(item.id)
        if item.name.title() not in self.__names:
            self.__categories[item.name.title()] = [item.id]
        else:
            self.__categories[item.name.title()].append(item.id)

    def get(self, item_id: str) -> MediaObject:
        if not isinstance(item_id, str):
            raise TypeError(
                f"ERROR: MediaCategory.get() takes only {str} type argument, not {type(item_id)}.\n"
            )
        if not self.__contains__(item_id):
            raise ObjectNotFoundError(
                f"ERROR: Object with id \"{item_id}\" is not found in catalog while trying to get it.\n"
            )
        return self.__data[item_id]

    def remove(self, item_id: str) -> MediaObject:
        if not isinstance(item_id, str):
            raise TypeError(
                f"ERROR: MediaCategory.remove() takes only {str} type argument, not {type(item_id)}.\n"
            )
        if not self.__contains__(item_id):
            raise ObjectNotFoundError(
                f"ERROR: Object with id \"{item_id}\" is not found in catalog while trying to remove it.\n"
            )
        value: MediaObject = self.__data.pop(item_id)
        return value

    def find_by_category(self, category: str) -> list[str]:
        if not isinstance(category, str):
            raise TypeError(
                f"ERROR: MediaCategory.find_by_category() takes only {str} type argument, not {type(category)}.\n"
            )
        if category.title() not in self.__categories:
            return []
        else:
            return self.__categories[category.title()][:]

    def find_by_name(self, query: str) -> list[str]:
        if not isinstance(query, str):
            raise TypeError(
                f"ERROR: MediaCategory.find_by_name() takes only {str} type argument, not {type(query)}.\n"
            )
        if query.title() not in self.__categories:
            return []
        else:
            return self.__names[query.title()][:]
