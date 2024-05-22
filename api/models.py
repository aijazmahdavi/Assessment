from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted = True
        self.save()

class BaseModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)

class ProjectPermission(BaseModel):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='permissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    can_create = models.BooleanField(default=False)
    can_read = models.BooleanField(default=False)
    can_update = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.project.name}"

class Project(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField()

    objects = BaseModelManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for permission in self.permissions.all():
            self.assign_permissions(permission.user, permission)

    def assign_permissions(self, user, permission):
        content_type = ContentType.objects.get_for_model(Task)
        task_permissions = Permission.objects.filter(content_type=content_type)

        if permission.can_create:
            user.user_permissions.add(*task_permissions.filter(codename__endswith='add_task'))

        if permission.can_read:
            user.user_permissions.add(*task_permissions.filter(codename__endswith='view_task'))

        if permission.can_update:
            user.user_permissions.add(*task_permissions.filter(codename__endswith='change_task'))

        if permission.can_delete:
            user.user_permissions.add(*task_permissions.filter(codename__endswith='delete_task'))


class Task(BaseModel):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    due_date = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', null=True)

    objects = BaseModelManager()

    def __str__(self):
        return self.title