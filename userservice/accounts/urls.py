from django.urls import include, path
from rest_framework import routers
from .api import (UserViewSet, UserDocumentViewSet, RoleViewSet, DepartmentViewSet)


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'user-documents', UserDocumentViewSet, basename='userdocument')
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'departments', DepartmentViewSet, basename='department')

urlpatterns = [
    path('', include(router.urls)),
]
