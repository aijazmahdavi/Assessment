from django.contrib import admin
from .models import *

# Register your models here.
# task admin
class TaskAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        # Limit the queryset to tasks created by the user or for the projects the user is part of
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user) | qs.filter(project__users=request.user)

    def save_model(self, request, obj, form, change):
        # Automatically assign the task to the user creating it
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        # Only allow the user to change tasks they own or are part of the project
        if obj and (obj.user == request.user or obj.project.users.filter(id=request.user.id).exists()):
            return True
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        # Only allow the user to delete tasks they own or are part of the project
        if obj and (obj.user == request.user or obj.project.users.filter(id=request.user.id).exists()):
            return True
        return super().has_delete_permission(request, obj)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'description',]
    list_filter = ['name', 'description', ]
    search_fields = ['name', 'description',]

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'status', 'due_date', 'project']
    list_filter = ['title', 'description', 'status', 'due_date', 'project']
    search_fields = ['title', 'description', 'status', 'due_date', 'project']