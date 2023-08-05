from rest_framework.mixins import UpdateModelMixin


class _HiddenAttributesMeta(type):
    """Raise AttributeError when accessing hidden_attributes on class itself"""

    def __getattribute__(self, name):
        if name in super().__getattribute__('hidden_attributes'):
            raise AttributeError(name)
        return super().__getattribute__(name)


class PutModelMixin(UpdateModelMixin, metaclass=_HiddenAttributesMeta):
    hidden_attributes = ['partial_update']
