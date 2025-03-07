from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Permission
from rest_framework.decorators import action
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from .models import (User, UserDocument, Role, Department)
from .serializers import (UserSerializer, UserListSerializer, UserDocumentSerializer, RoleSerializer,
         DepartmentSerializer, PermissionSerializer)

class UserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, 
                  mixins.RetrieveModelMixin):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        """Use different serializers for list, retrieve, create, and update."""
        if self.action in ["create", "update"]:
            return UserSerializer
        return UserListSerializer

    def list(self, request):
        """List all users."""
        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Retrieve a single user along with details."""
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Create a new user with optional details."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Update user details."""
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDocumentViewSet(viewsets.GenericViewSet,
                          mixins.CreateModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin):

    queryset = UserDocument.objects.filter(is_deleted=False)
    serializer_class = UserDocumentSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        """Handle soft deletion of the old document and create a new one"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        new_document = serializer.save()
        return Response(UserDocumentSerializer(new_document).data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """Soft delete the document instead of actually deleting it"""
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response({"message": "Document deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class RoleViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='available-permissions')
    def available_permissions(self, request):
        """
        Custom API endpoint to list all available permissions.
        """
        permissions = Permission.objects.all()
        serializer = PermissionSerializer(permissions, many=True)
        return Response(serializer.data)


class DepartmentViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
