from .catalogs_object import CatalogsObject

class LandTypes(CatalogsObject):
    """
    catalogs/land-types

    Catalog object for all known land types.

    Args:
        N/A

    Returns:
        N/A

    Raises:
        N/A

    Examples:
        >>> catalog = scrython.catalog.LandTypes()
        >>> catalog.data()
    """
    def __init__(self):
        self._url = 'catalog/land-types?'
        super(LandTypes, self).__init__(self._url)
