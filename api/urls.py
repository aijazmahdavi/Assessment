from django.urls import path, include
from rest_framework import routers
from .views import ProjectViewSet, TaskViewSet

router = routers.DefaultRouter()
router.register('projects', ProjectViewSet)
router.register('tasks', TaskViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]