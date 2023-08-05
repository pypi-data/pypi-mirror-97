try:
    from django.contrib.postgres.fields import ArrayField
except ImportError:
    ArrayField = None

import unicodedata

from django import forms
from django.core.validators import MinValueValidator
from django.db import models

from django_handy.objs import unique_ordered
from django_handy.validation import MinValueExclusionValidator


class LowerFieldDescriptor:
    def __init__(self, field):
        self.field = field

    def __get__(self, instance, owner=None):
        if instance is None:
            return None
        return instance.__dict__[self.field.attname]  # noqa: WPS609

    def __set__(self, instance, value):
        instance.__dict__[self.field.attname] = self.field.to_python(value)  # noqa: WPS609


class LowerCaseFieldMixin:
    def to_python(self, value):
        value = super().to_python(value)
        if value:
            value = unicodedata.normalize('NFKC', value)
            if hasattr(value, 'casefold'):  # noqa: WPS421
                value = value.casefold()
        return value

    def contribute_to_class(self, cls, name, **kwargs):  # noqa: WPS117
        super().contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.attname, LowerFieldDescriptor(self))


class EmailLowerCaseField(LowerCaseFieldMixin, models.EmailField):
    pass


class PositiveDecimalField(models.DecimalField):
    default_validators = [MinValueValidator(0)]

    def __init__(self, no_zero=False, **kwargs):
        if no_zero:
            validators = kwargs.pop('validators', [])
            validators.append(MinValueExclusionValidator(0))
            kwargs['validators'] = validators
        super().__init__(**kwargs)


if ArrayField:
    class UniqueArrayField(ArrayField):
        """Ensures that no duplicates are saved to database"""

        def get_db_prep_value(self, value, connection, prepared=False):
            if isinstance(value, (list, tuple)):
                value = unique_ordered(value)
            return super().get_db_prep_value(value, connection, prepared)


    class ChoicesUniqueArrayField(UniqueArrayField):
        def formfield(self, **kwargs):
            defaults = {
                'form_class': forms.TypedMultipleChoiceField,
                'choices': self.base_field.choices,
                'coerce': self.base_field.to_python,
                'widget': forms.CheckboxSelectMultiple,
            }
            defaults.update(kwargs)
            # This super() call is intentional to jump over ArrayField.formfield
            return super(ArrayField, self).formfield(**defaults)
