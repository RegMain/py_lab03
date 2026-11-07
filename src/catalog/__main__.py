from catalog.models import MediaCatalog


def main():
    """
    catalog = MediaCatalog()
    for i in range(5):
        catalog.add(MediaObject(
            f"id{i}",
            "133",
            "naa",
            "444",
            "aerr",
            i+1,
            i+1,
            2026
        ))
    catalog.dump()"""
    catalog = MediaCatalog()
    catalog.load()
    catalog.dump("catalog(1).json")


if __name__ == "__main__":
    main()
