from django.contrib import admin
from .models import *

# Register your models here.
# task admin
class TaskAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'project' in form.base_fields:
            form.base_fields['project'].queryset = Project.objects.filter(permissions__user=request.user)
        return form

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if obj and obj.project.permissions.filter(user=request.user, can_update=True).exists():
            return True
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.project.permissions.filter(user=request.user, can_delete=True).exists():
            return True
        return super().has_delete_permission(request, obj)

    list_display = ['title', 'description', 'status', 'due_date', 'project']
    list_filter = ['title', 'description', 'status', 'due_date', 'project']
    search_fields = ['title', 'description', 'status', 'due_date', 'project']


# inlines
class ProjectPermissionInline(admin.TabularInline):
    model = ProjectPermission
    extra = 1



@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'description',]
    list_filter = ['name', 'description', ]
    search_fields = ['name', 'description',]
    inlines = [ProjectPermissionInline]

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'project' in form.base_fields:
            form.base_fields['project'].queryset = Project.objects.filter(permissions__user=request.user)
        return form



