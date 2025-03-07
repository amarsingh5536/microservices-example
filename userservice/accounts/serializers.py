import uuid
import random
import string
from rest_framework import serializers
from django.contrib.auth.models import Permission
from .models import (User, UserDetail, UserDocument, Department, Role)

def generate_random_password(length=12):
    """Generate a secure random password."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = ["phone_number", "address", "date_of_birth"]

class UserSerializer(serializers.ModelSerializer):
    details = UserDetailSerializer(required=False)
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.filter(parent=None), required=False, allow_null=True)
    sub_department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.exclude(parent=None), required=False, allow_null=True)
    role = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), required=False, allow_null=True)

    class Meta:
        model = User
        fields = ["id", "email", "username", "first_name", "last_name", "password", "department", "sub_department", "role", "details"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        details_data = validated_data.pop("details")
        password = validated_data.pop("password")  or  generate_random_password()

        user = User.objects.create(**validated_data)
        user.set_password(password)  # Hash password
        user.save()

        UserDetail.objects.create(user=user, **details_data)

        return user

    def update(self, instance, validated_data):
        details_data = validated_data.pop("details", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data:
            UserDetail.objects.update_or_create(user=instance, defaults=details_data)

        return instance

class UserListSerializer(serializers.ModelSerializer):
    details = UserDetailSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "department", "role", "details"]


class UserDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDocument
        fields = ['id', 'user', 'document_type', 'document', 'document_name', 'is_deleted', 'created_at', 'uploaded_at']
        read_only_fields = ['document_name', 'created_at', 'uploaded_at']

    def create(self, validated_data):
        user = validated_data['user']
        document_type = validated_data['document_type']

        # Mark previous documents of the same type as deleted
        UserDocument.objects.filter(user=user, document_type=document_type, is_deleted=False).update(is_deleted=True)
        validated_data['document_name'] = str(uuid.uuid4())
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Update the document by soft deleting the old one and creating a new entry"""
        user = instance.user
        document_type = instance.document_type

        # Soft delete previous document of the same type
        instance.is_deleted = True
        instance.save()

        # Create a new document entry
        new_document = UserDocument.objects.create(
            user=user,
            document_type=document_type,
            document=validated_data.get('document', instance.document),
            document_name=str(uuid.uuid4())
        )
        return new_document


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "name", "codename", "content_type"]

class RoleSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True)

    class Meta:
        model = Role
        fields = ["id", "name", "permissions"]

class DepartmentSerializer(serializers.ModelSerializer):
    parent_name = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ["id", "name", "parent", "parent_name"]

    def get_parent_name(self, obj):
        return obj.parent.name if obj.parent else None