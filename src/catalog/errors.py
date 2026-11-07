class CatalogError(Exception):
    pass


class InvalidObjectError(CatalogError):
    pass


class IDDuplicateError(CatalogError):
    pass


class ObjectNotFoundError(CatalogError):
    pass


class IncompatibleVersionError(CatalogError):
    pass


class BrokenFileError(CatalogError):
    pass
