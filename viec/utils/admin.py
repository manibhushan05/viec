from datetime import datetime

from django.contrib import admin

from utils.models import Country, State


class CountryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code', 'dial_code']
    search_fields = ['id', 'name', 'code', 'dial_code']
    list_filter = ['deleted']
    empty_value_display = 'unknown'

    def get_readonly_fields(self, request, obj=None):
        return ['created_on', 'updated_on']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.deleted = True
        obj.deleted_on = datetime.now()
        super().delete_model(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return True


class StateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code')
    search_fields = ['id', 'name', 'code']
    list_filter = ['deleted']
    empty_value_display = 'unknown'
    autocomplete_fields = ('country',)

    def get_readonly_fields(self, request, obj=None):
        return ['created_on', 'updated_on']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.deleted = True
        obj.deleted_on = datetime.now()
        super().delete_model(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.deleted:
            return False
        return True


admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)
