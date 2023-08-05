from typing import List

from django.db import models

from rest_framework import serializers


# noinspection PyAbstractClass
class EmptySerializer(serializers.Serializer):
    pass


# noinspection PyUnresolvedReferences
class SerializerRequestMixin:
    @property
    def request(self):
        return self.context['request']


class SelectObjectsSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField(min_value=0))

    @property
    def selected_ids(self) -> List[int]:
        return self.validated_data.get('ids', [])

    @property
    def selected_objects(self) -> models.QuerySet:
        objects = self.context['view'].get_queryset()
        objects = objects.filter(id__in=self.selected_ids)
        return objects
