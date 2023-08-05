from typing import Iterable
from typing import List
from typing import Type

from django.db import models


def get_update_fields(cls: Type[models.Model], exclude: Iterable[str] = None) -> List[str]:
    exclude = set(exclude) if exclude is not None else {}

    def _can_be_updated(field):
        return (
            field.name not in exclude and
            not (field.many_to_many or field.one_to_many)
            and not field.auto_created
        )

    return [
        field.name for field in cls._meta.get_fields()
        if _can_be_updated(field)
    ]
