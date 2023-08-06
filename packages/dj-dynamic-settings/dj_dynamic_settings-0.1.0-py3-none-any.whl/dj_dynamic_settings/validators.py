from django.core.exceptions import ValidationError
from django.utils.module_loading import import_string


class TypeValidator(object):
    message = "'{value}' not an instance of one of classes '{types}'."

    def __init__(self, *types):
        assert types, "At least one class have to be provided."
        self.types = types

    def __call__(self, value):
        if not isinstance(value, self.types):
            raise ValidationError(self.message.format(value=value, types=self.types))


class ModulePathValidator(object):
    message = "{path} not a valid module path."

    def __call__(self, value):
        try:
            import_string(value)
        except ImportError:
            raise ValidationError(self.message.format(path=value))


class SerializerValidator(object):
    def __init__(self, serializer_class, serializer_kwargs=None):
        self.serializer_class = serializer_class
        self.serializer_kwargs = serializer_kwargs or {}

    def __call__(self, value):
        serializer = self.serializer_class(data=value, **self.serializer_kwargs)
        serializer.is_valid(raise_exception=True)
