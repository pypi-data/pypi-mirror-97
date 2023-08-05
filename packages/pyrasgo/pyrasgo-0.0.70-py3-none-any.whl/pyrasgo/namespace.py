from types import SimpleNamespace


class Namespace(SimpleNamespace):
    """
    Extended SimpleNamespace to allow for recursive dictionaries
    """

    def __init__(self, **kwargs):
        """Create a SimpleNamespace recursively"""
        super().__init__()
        self.__dict__.update({k: self.__parse(v) for k, v in kwargs.items()})

    def __parse(self, struc):
        """Recurse into nested data structure to create leaf namespace objects"""
        if type(struc) is dict:
            return type(self)(**struc)
        if type(struc) in (list, tuple):
            return [self.__parse(i) for i in struc]
        return struc

    def __unparse(self, value):
        if isinstance(value, type(self)):
            return value.to_dict()
        if type(value) in (list, tuple):
            return [self.__unparse(i) for i in value]
        if value is None:
            return
        return value

    def to_dict(self):
        return {k: self.__unparse(v) or 'null' for k, v in self.__dict__.items()}
