from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render

# for project and tasks
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework import permissions

# Task form
from .forms import TaskForm

# Login auth JWT
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                'access_token': access_token,
                'refresh_token': refresh_token
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=401)


# check if user has permission to create task in project
class IsProjectUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['create', 'list']:
            project_id = request.data.get('project') if view.action == 'create' else view.kwargs.get('project_id')
            if project_id:
                project = Project.objects.get(id=project_id)
                return request.user in project.users.all()
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Task):
            project = obj.project
        elif isinstance(obj, Project):
            project = obj
        return request.user in project.users.all()

# Projects and tasks
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        project = serializer.save()
        project.users.add(self.request.user)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsProjectUser]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(project__users=user)

    def perform_create(self, serializer):
        project = Project.objects.get(id=self.request.data['project'])
        if self.request.user in project.users.all():
            serializer.save(user=self.request.user)
        else:
            raise PermissionDenied("You don't have permission to create tasks for this project.")

    def perform_update(self, serializer):
        project = serializer.instance.project
        if self.request.user in project.users.all():
            serializer.save()
        else:
            raise PermissionDenied("You don't have permission to update tasks for this project.")

    def perform_destroy(self, instance):
        project = instance.project
        if self.request.user in project.users.all():
            instance.delete()
        else:
            raise PermissionDenied("You don't have permission to delete tasks for this project.")





def create_task(request):
    form = TaskForm(user=request.user)  # Pass the user information to the form
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)  # Pass the user information again when processing the form
        if form.is_valid():
            form.save()
            # Redirect or do something else
    return render(request, 'create_task.html', {'form': form})