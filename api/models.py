from django.db import models
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    users = models.ManyToManyField(User, related_name='projects')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for user in self.users.all():
            assign_task_permissions(user)

def assign_task_permissions(user):
    content_type = ContentType.objects.get_for_model(Task)
    permissions = Permission.objects.filter(content_type=content_type)
    user.user_permissions.add(*permissions)

@receiver(m2m_changed, sender=Project.users.through)
def users_changed(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        for user in instance.users.all():
            assign_task_permissions(user)

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    due_date = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title
