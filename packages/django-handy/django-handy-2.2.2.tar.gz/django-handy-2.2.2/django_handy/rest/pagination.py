from django.core.paginator import Paginator as DjangoPaginator
from django.utils.functional import cached_property
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from django_handy.models import get_count


class DefaultPaginator(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 300

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'page': self.page.number,
            self.page_size_query_param: self.get_page_size(self.request),
            'results': data,
        })


class OptimizedDjangoPaginator(DjangoPaginator):
    @cached_property
    def count(self):
        return get_count(self.object_list)


class OptimizedDefaultPaginator(DefaultPaginator):
    django_paginator_class = OptimizedDjangoPaginator


class OptimizedLimitOffsetPaginator(LimitOffsetPagination):
    def get_count(self, queryset):
        return get_count(queryset)
