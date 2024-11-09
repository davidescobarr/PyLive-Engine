from core.utils.delegates.PropertyValueDelegate import property_value_delegate


class VisibleValue:
    def __init__(self, path='', is_visible=True):
        self._path = path
        self._is_visible = is_visible
        self.fget = None
        self.fset = None

    def __call__(self, func):
        if not self.fget:
            self.fget = func
        else:
            self.fset = func
        return self

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self.fget is None:
            raise AttributeError("Unreadable attribute: no getter defined")
        return self.fget(instance)

    def __set__(self, instance, value):
        if self.fset is None:
            raise AttributeError("Can't set attribute: no setter defined")
        self.fset(instance, value)
        property_value_delegate.notify(self)

    def getter(self, fget):
        self.fget = fget
        return self

    def setter(self, fset):
        self.fset = fset
        return self

    @classmethod
    def extract_path(cls, path, prop, value):
        keys = path.rstrip('/').split('/')
        d = {prop: value}
        for key in reversed(keys):
            d = {key: d}
        return d

    @classmethod
    def find_visible_properties(cls, instance):
        visible_properties = []
        for name, attr in instance.__class__.__dict__.items():
            if isinstance(attr, cls):
                value = getattr(instance, name)
                if attr._is_visible:
                    visible_properties.append((attr._path, name, value))
        return visible_properties

    @classmethod
    def aggregate_properties(cls, instance, properties):
        aggregated = {}
        for path, prop, value in properties:
            d = cls.extract_path(path, prop, value)
            aggregated = cls.merge_dicts(aggregated, d)
        return aggregated

    @staticmethod
    def merge_dicts(a, b):
        for key in b:
            if key in a and isinstance(a[key], dict) and isinstance(b[key], dict):
                a[key] = VisibleValue.merge_dicts(a[key], b[key])
            else:
                a[key] = b[key]
        return a
