from dataclasses import asdict

import pytest

from catalog.errors import InvalidObjectError, IDDuplicateError, BrokenFileError, IncompatibleVersionError
from catalog.models import MediaObject, MediaCatalog

def test_correct_object():
    expected = {
        "id": "id0",
        "category": "Music",
        "name": "Never Gonna Give You Up",
        "genre": "Dance-Pop",
        "author": "Rick Astley",
        "duration": 213000,
        "size": 3145728,
        "year": 1987,
    }
    result = MediaObject(
        "id0",
        "music",
        "Never Gonna Give You Up",
        "Dance-pop",
        "Rick Astley",
        213000,
        3145728,
        1987,
    )
    assert expected == asdict(result)


def test_incorrect_object():
    with pytest.raises(InvalidObjectError):
        MediaObject(
            "",
            "music",
            "Never Gonna Give You Up",
            "Dance-pop",
            "Rick Astley",
            213000,
            3145728,
            1987,
        )
    with pytest.raises(InvalidObjectError):
        MediaObject(
            "id0",
            13,
            "Never Gonna Give You Up",
            "Dance-pop",
            "Rick Astley",
            213000,
            3145728,
            1987,
        )
    with pytest.raises(InvalidObjectError):
        MediaObject(
            "id0",
            "music",
            "Never Gonna Give You Up",
            "Dance-pop",
            "Rick Astley",
            245.53,
            3145728,
            1987,
        )
    with pytest.raises(InvalidObjectError):
        MediaObject(
            "id0",
            "music",
            "Never Gonna Give You Up",
            "Dance-pop",
            "Rick Astley",
            213000,
            -1,
            1987,
        )

def test_add_get_remove():
    object = MediaObject(
        "id0", "music", "Never Gonna Give You Up",
        "Dance-pop", "Rick Astley", 213000, 3145728,
        1987
    )
    catalog = MediaCatalog()
    catalog.add(object)
    assert object == catalog.get("id0")

def test_duplicate_id():
    with pytest.raises(IDDuplicateError):
        object = MediaObject(
            "id0", "music", "Never Gonna Give You Up",
            "Dance-pop", "Rick Astley", 213000, 3145728,
            1987
        )
        catalog = MediaCatalog()
        catalog.add(object)
        catalog.add(object)

def test_find_by_category():
    catalog = MediaCatalog()
    i = 0
    for category in ["music", "music", "movie", "music", "movie"]:
        i += 1
        obj = MediaObject(f"id{i}", category, "abc", "abc", "abc", 111, 111, 111)
        catalog.add(obj)
    assert catalog.find_by_category("music") == ["id1", "id2", "id4"]
    assert catalog.find_by_category("movie") == ["id3", "id5"]

def test_find_by_name():
    catalog = MediaCatalog()
    i = 0
    for name in ["abc", "abc", "5", "5", "abc"]:
        i += 1
        obj = MediaObject(f"id{i}", "music", name, "111", "111", 111, 111, 111)
        catalog.add(obj)
    assert catalog.find_by_name("abc") == ["id1", "id2", "id5"]
    assert catalog.find_by_name("5") == ["id3", "id4"]

def test_iteration_order():
    catalog = MediaCatalog()
    i = 0
    for name in ["abc", "abc", "5", "5", "abc"]:
        i += 1
        obj = MediaObject(f"id{i}", "music", name, "111", "111", 111, 111, 111)
        catalog.add(obj)
    catalog.add(MediaObject("id0", "music", name, "100", "1", 3, 3, 113))
    result = []
    expected = ["id1", "id2", "id3", "id4", "id5", "id0"]
    for obj in catalog:
        result.append(obj.id)
    assert result == expected

def test_round_trip_json(tmp_path):
    catalog = MediaCatalog()
    i = 0
    for name in ["abc", "abc", "5", "5", "abc"]:
        i += 1
        obj = MediaObject(f"id{i}", "music", name, "111", "111", 111, 111, 111)
        catalog.add(obj)
    catalog.dump(str(tmp_path / "catalog.json"))
    json_catalog = MediaCatalog()
    json_catalog.load(str(tmp_path / "catalog.json"))
    assert catalog == json_catalog

def test_broken_json():
    with pytest.raises(BrokenFileError):
        catalog = MediaCatalog()
        catalog.load("tests/broken_catalog.json")

def test_unknown_version_json():
    with pytest.raises(IncompatibleVersionError):
        catalog = MediaCatalog()
        catalog.load("tests/unknown_version_catalog.json")

def test_after_load_error():
    catalog = MediaCatalog()
    broken_catalog = MediaCatalog()
    try:
        broken_catalog.load("tests/broken_catalog.json")
    except BrokenFileError:
        pass
    assert catalog == broken_catalog
