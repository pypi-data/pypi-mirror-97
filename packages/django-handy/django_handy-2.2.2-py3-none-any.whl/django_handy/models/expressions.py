from django.core.exceptions import EmptyResultSet
from django.db import models
from django.db.models import Avg
from django.db.models import BooleanField
from django.db.models import Count
from django.db.models import ExpressionWrapper
from django.db.models import Max
from django.db.models import Min
from django.db.models import Subquery
from django.db.models import Sum
from django.db.models import Value


class BooleanQ(ExpressionWrapper):
    output_field = BooleanField()

    def __init__(self, *args, **kwargs):
        expression = models.Q(*args, **kwargs)
        super().__init__(expression, output_field=None)

    def as_sql(self, compiler, connection):
        try:
            return super().as_sql(compiler, connection)
        except EmptyResultSet:
            return compiler.compile(Value(False))


class SubqueryAgg(Subquery):
    template = '(SELECT %(func)s(%(field_name)s) FROM (%(subquery)s) _sub)'

    def __init__(self, queryset, field_name, func, **kwargs):
        queryset = queryset.order_by()
        if not queryset.query.values_select:
            queryset = queryset.values(field_name)
        super().__init__(queryset, field_name=field_name, func=func, **kwargs)


class SubqueryAvg(SubqueryAgg):
    def __init__(self, queryset, field_name, **kwargs):
        super().__init__(queryset, field_name, func=Avg.function, **kwargs)


class SubqueryMin(SubqueryAgg):
    def __init__(self, queryset, field_name, **kwargs):
        super().__init__(queryset, field_name, func=Min.function, **kwargs)


class SubqueryMax(SubqueryAgg):
    def __init__(self, queryset, field_name, **kwargs):
        super().__init__(queryset, field_name, func=Max.function, **kwargs)


class SubquerySum(SubqueryAgg):
    def __init__(self, queryset, field_name, **kwargs):
        super().__init__(queryset, field_name, func=Sum.function, **kwargs)


class SubqueryCount(SubqueryAgg):
    output_field = models.IntegerField()

    def __init__(self, queryset, **kwargs):
        if not queryset.query.values_select:
            queryset = queryset.values('pk')
        super().__init__(queryset, field_name='*', func=Count.function, **kwargs)
