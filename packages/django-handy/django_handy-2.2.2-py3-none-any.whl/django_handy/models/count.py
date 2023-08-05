def get_count(queryset):
    """Determine an object count in optimized manner. Incompatible with custom values/distinct/group by"""
    try:
        return queryset.values('pk').order_by().count()
    except (AttributeError, TypeError):
        return len(queryset)
