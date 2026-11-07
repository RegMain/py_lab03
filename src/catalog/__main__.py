import sys
from catalog.models import MediaCatalog, MediaObject
from catalog.errors import CatalogError
from catalog.constants import CURRENT_VERSION, MEDIA_OBJECT_FIELD_TYPES

def demo_add(catalog: MediaCatalog):
    object = {}
    for field_type, field_value_type in MEDIA_OBJECT_FIELD_TYPES.items():
        object[field_type] = field_value_type(input(f"Input {field_value_type} value for MediaObject field \"{field_type}\": "))
    catalog.add(MediaObject(**object))
    print()

def demo_remove(catalog: MediaCatalog):
    id = input("Input id to remove: ")
    catalog.remove(id)
    print()

def demo_get(catalog: MediaCatalog):
    id = input("Input id to get: ")
    print(catalog.get(id))
    print()

def demo_find_by_name(catalog: MediaCatalog):
    name = input("Input name to find: ")
    print(*catalog.find_by_name(name))
    print()

def demo_find_by_category(catalog: MediaCatalog):
    category = input("Input category to find: ")
    print(*catalog.find_by_category(category))
    print()

def demo_dump(catalog: MediaCatalog):
    path = input("Input path to file to write to: ")
    catalog.dump(path)
    print()

def demo_load(catalog: MediaCatalog):
    path = input("Input path to file to read from: ")
    catalog.load(path)
    print()

def demo_check(catalog: MediaCatalog):
    id = input("Input id to check for containment: ")
    if id in catalog:
        print("YES")
    else:
        print("NO")
    print()

def demo_version():
    print(CURRENT_VERSION)
    print()

def main():
    print("Demonstration of work\n")
    catalog = MediaCatalog()
    while True:
        print("[1] Add to catalog")
        print("[2] Remove from catalog")
        print("[3] Get object by id")
        print("[4] Find by name")
        print("[5] Find by category")
        print("[6] Dump to json")
        print("[7] Load to json")
        print("[8] Check is object in catalog by id")
        print("[9] Print version")
        key = input("Enter option (1..9). Print something else to quit: ")
        try:
            match key:
                case "1": demo_add(catalog)
                case "2": demo_remove(catalog)
                case "3": demo_get(catalog)
                case "4": demo_find_by_name(catalog)
                case "5": demo_find_by_category(catalog)
                case "6": demo_dump(catalog)
                case "7": demo_load(catalog)
                case "8": demo_check(catalog)
                case "9": demo_version()
                case _: sys.exit(0)
        except CatalogError as err:
            print(err)
            sys.exit(2)

if __name__ == "__main__":
    main()
