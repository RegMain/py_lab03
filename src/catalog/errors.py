class CatalogError(Exception):
    pass

class InvalidObjectError(CatalogError):
    pass

class IDDuplicateError(CatalogError):
    pass

class ObjectNotFound(CatalogError):
    pass

class UnsupportedVersionError(CatalogError):
    pass

class BrokenFileError(CatalogError):
    pass
