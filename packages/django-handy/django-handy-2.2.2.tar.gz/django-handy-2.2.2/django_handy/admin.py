from itertools import chain

from django.contrib.admin.utils import flatten_fieldsets
from django.db.models.fields import Field
from django.urls import reverse
from django.utils.inspect import get_func_args


def object_admin_rel_url(obj):
    return reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=(obj.pk,))


class ReadOnlyFieldsAdminMixin:
    editable_fields = []
    exclude = []

    def get_readonly_fields(self, request, obj=None):
        args = get_func_args(self.has_add_permission)
        if 'obj' in args:
            has_add_permission = self.has_add_permission(request, obj)
        else:
            has_add_permission = self.has_add_permission(request)

        if obj is None and has_add_permission:
            return super().get_readonly_fields(request, obj)

        if self.fields or self.fieldsets:
            fields = flatten_fieldsets(self.get_fieldsets(request, obj))
        else:
            opts = self.model._meta
            sortable_private_fields = [f for f in opts.private_fields if isinstance(f, Field)]

            fields = [
                field.name for field in
                sorted(chain(opts.concrete_fields, sortable_private_fields, opts.many_to_many))
                if field.editable and not field.auto_created
            ]

        exclude = self.get_exclude(request, obj)
        editable_fields = self.get_editable_fields(request, obj)
        return [
            field for field in fields
            if field not in editable_fields and field not in exclude
        ]

    def get_editable_fields(self, request, obj=None):
        return self.editable_fields


class NoAddDeleteAdminMixin:
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ReadOnlyAdminMixin(NoAddDeleteAdminMixin):
    def has_change_permission(self, request, obj=None):
        return False
