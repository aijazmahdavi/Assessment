# In your forms.py

from django import forms
from .models import Task, Project

class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['project'].queryset = Project.objects.filter(users=user)

    class Meta:
        model = Task
        fields = '__all__'
