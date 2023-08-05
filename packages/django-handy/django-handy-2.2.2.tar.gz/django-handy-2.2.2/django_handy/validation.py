from PIL import Image
from django.core.validators import BaseValidator
from django.forms import forms
from django.template.defaultfilters import filesizeformat
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext as _


class MinValueExclusionValidator(BaseValidator):
    message = _('Ensure this value is greater than %(limit_value)s')
    code = 'min_value_exclusive'

    def compare(self, a, b):
        return a <= b


class MaxValueExclusionValidator(BaseValidator):
    message = _('Ensure this value is less than %(limit_value)s')
    code = 'max_value_exclusive'

    def compare(self, a, b):
        return a >= b


@deconstructible
class FileSizeValidator:
    def __init__(self, max_size):
        self.max_size = max_size

    def __call__(self, value):
        if value.size > self.max_size:
            raise forms.ValidationError(
                _('Maximum allowed size is %(max_size)s') % {'max_size': filesizeformat(self.max_size)}
            )


@deconstructible
class ImageSizeValidator(FileSizeValidator):
    def __init__(self, max_size, max_pixels):
        super().__init__(max_size=max_size)
        self.max_pixels = max_pixels

    def __call__(self, value):
        super().__call__(value)

        try:
            image = value.image
        except AttributeError:
            image = Image.open(value)

        dimensions = image.size
        if dimensions[0] > self.max_pixels:
            raise forms.ValidationError(
                _('Maximum allowed width is %(max_pixels)spx') % {'max_pixels': self.max_pixels}
            )
        elif dimensions[1] > self.max_pixels:
            raise forms.ValidationError(
                _('Maximum allowed height is %(max_pixels)spx') % {'max_pixels': self.max_pixels}
            )
