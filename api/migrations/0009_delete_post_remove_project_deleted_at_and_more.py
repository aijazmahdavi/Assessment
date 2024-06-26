# Generated by Django 5.0.6 on 2024-05-21 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_post'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.RemoveField(
            model_name='project',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='project',
            name='restored_at',
        ),
        migrations.RemoveField(
            model_name='task',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='task',
            name='restored_at',
        ),
        migrations.AddField(
            model_name='project',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='task',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
