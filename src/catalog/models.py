import json
from dataclasses import asdict, dataclass, is_dataclass

from catalog.constants import (
    COMPATIBLE_VERSIONS,
    CURRENT_VERSION,
    MEDIA_OBJECT_FIELD_TYPES,
)
from catalog.errors import (
    BrokenFileError,
    IDDuplicateError,
    IncompatibleVersionError,
    InvalidObjectError,
    ObjectNotFoundError,
)


class DataclassJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if is_dataclass(o):
            return asdict(o)
        return super().default(o)


@dataclass
class MediaObject:
    id: str  # Unique
    category: str
    name: str
    genre: str
    author: str
    duration: int  # time in ms
    size: int  # size in bytes
    year: int

    def check(self) -> None:
        for attr in vars(self):
            field_type = MEDIA_OBJECT_FIELD_TYPES[attr]
            object_field_value = getattr(self, attr)
            if not isinstance(object_field_value, field_type):
                raise InvalidObjectError(
                    f'ERROR: Object field "{attr}" should have type {field_type}, not {type(object_field_value)}.\n'
                )
            if not object_field_value:
                raise InvalidObjectError(
                    f'ERROR: Object field "{attr}" should have a valid value.\n'
                )
            if (attr != "id") and isinstance(object_field_value, str):
                setattr(self, attr, object_field_value.title())
        if self.size < 0:
            raise InvalidObjectError(
                "ERROR: Object size cannot be less than zero bytes.\n"
            )

    def __post_init__(self) -> None:
        self.check()


class MediaCatalog:
    __data: dict[str, MediaObject]
    __categories: dict[str, list[str]]
    __names: dict[str, list[str]]

    def __init__(self) -> None:
        self.__data = {}
        self.__categories = {}
        self.__names = {}

    def __len__(self) -> int:
        return len(self.__data)

    def __eq__(self, other) -> bool:
        for attr in vars(self):
            try:
                if getattr(self, attr) != getattr(other, attr):
                    return False
            except AttributeError:
                return False
        return True

    def __iter__(self):
        return iter(self.__data.values())

    def __contains__(self, item_id: str) -> bool:
        return item_id in self.__data

    def add(self, item: MediaObject) -> None:
        if not isinstance(item, MediaObject):
            raise InvalidObjectError(
                "ERROR: Trying to insert non MediaObject type object in catalog.\n"
            )
        if self.__contains__(item.id):
            raise IDDuplicateError(
                f'ERROR: Trying to insert object with existing id "{item.id}" in catalog.\n'
            )
        self.__data[item.id] = item
        if item.category.title() not in self.__categories:
            self.__categories[item.category.title()] = [item.id]
        else:
            self.__categories[item.category.title()].append(item.id)
        if item.name.title() not in self.__names:
            self.__names[item.name.title()] = [item.id]
        else:
            self.__names[item.name.title()].append(item.id)

    def get(self, item_id: str) -> MediaObject:
        if not isinstance(item_id, str):
            raise TypeError(
                f"ERROR: MediaCategory.get() takes only {str} type argument, not {type(item_id)}.\n"
            )
        if not self.__contains__(item_id):
            raise ObjectNotFoundError(
                f'ERROR: Object with id "{item_id}" is not found in catalog while trying to get it.\n'
            )
        return self.__data[item_id]

    def remove(self, item_id: str) -> MediaObject:
        if not isinstance(item_id, str):
            raise TypeError(
                f"ERROR: MediaCategory.remove() takes only {str} type argument, not {type(item_id)}.\n"
            )
        if not self.__contains__(item_id):
            raise ObjectNotFoundError(
                f'ERROR: Object with id "{item_id}" is not found in catalog while trying to remove it.\n'
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
        if query.title() not in self.__names:
            return []
        else:
            return self.__names[query.title()][:]

    def dump(self, filename: str = "catalog.json") -> None:
        try:
            with open(filename, "w") as file:
                json.dump(
                    {"version": CURRENT_VERSION, "data": self.__data},
                    file,
                    indent=2,
                    cls=DataclassJSONEncoder,
                )
        except OSError:
            raise BrokenFileError(
                f"File {filename} is either not exists or you have no permission to read it or it is a directory.\n"
            )
        except json.JSONDecodeError:
            raise BrokenFileError(
                f"File {filename} is either broken or has wrong format.\n"
            )

    def load(self, filename: str = "catalog.json") -> None:
        try:
            with open(filename, "r") as file:
                try:
                    json_data = json.load(file)
                except json.JSONDecodeError:
                    raise BrokenFileError(
                        f"File {filename} is either broken or has wrong format.\n"
                    )
                if (
                    "version" not in json_data
                    or "data" not in json_data
                    or len(json_data) != 2
                ):
                    raise BrokenFileError(
                        f"File {filename} is either broken or has wrong format.\n"
                    )
                if json_data["version"] not in COMPATIBLE_VERSIONS:
                    raise IncompatibleVersionError(
                        f"Version {json_data['version']} is incompatible with version {CURRENT_VERSION} of catalog.\n"
                    )
                json_categories = {}
                json_names = {}
                for id, object in json_data["data"].items():
                    try:
                        json_data["data"][id] = MediaObject(**object)
                    except (InvalidObjectError, TypeError):
                        raise BrokenFileError(f"File {filename} is broken.\n")
                    if object["category"] not in json_categories:
                        json_categories[object["category"]] = []
                    json_categories[object["category"]].append(id)
                    if object["name"] not in json_names:
                        json_names[object["name"]] = []
                    json_names[object["name"]].append(id)
                self.__data = json_data["data"]
                self.__categories = json_categories
                self.__names = json_names
        except OSError:
            raise BrokenFileError(
                f"File {filename} is either not exists or you have no permission to read it or it is a directory.\n"
            )
