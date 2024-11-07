from core.utils.delegates.PropertyValueDelegate import property_value_delegate


class VisibleValue:
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self._is_visible = True  # Adding a visibility flag
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self.fget is None:
            raise AttributeError("Unreadable attribute")
        return self.fget(instance)

    def __set__(self, instance, value):
        if self.fset is None:
            raise AttributeError("Can't set attribute")
        # Notify the delegate before setting the value
        self.fset(instance, value)
        property_value_delegate.notify(self)

    def getter(self, fget):
        """Allows specifying a custom getter function."""
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        """Allows specifying a custom setter function."""
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        """Allows specifying a custom deleter function."""
        return type(self)(self.fget, self.fset, fdel, self.__doc__)

    @classmethod
    def find_visible_properties(cls, instance):
        """Finds all properties marked as visible in the given instance."""
        visible_properties = []
        for name, attr in instance.__class__.__dict__.items():
            if getattr(attr, "_is_visible", False):
                visible_properties.append((name, getattr(instance, name)))
        return visible_properties