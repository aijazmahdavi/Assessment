from django.contrib import admin
from .models import *

# Register your models here.

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