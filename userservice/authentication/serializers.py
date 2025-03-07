import random
from decouple import config 
from datetime import timedelta
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from accounts.models import (OTP, User)
from .utils import EMAIL_REGEX


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'username'
    
    default_error_messages = {
        "no_active_account": _("Invalid username or password."),
    }

    def __init__(self, *args, **kwargs):
        """
        Initialize the serializer with dynamic fields and access token lifetime.
        """
        super().__init__(*args, **kwargs)
        self.fields[self.username_field].help_text = 'Email / Username / Phone Number'
        
        # Set default token lifetime or override using "remember_me"
        self.access_token_lifetime = timezone.timedelta(
            minutes=int(config('FALSE_TOKEN_LIFETIME', default=30))
        )

    def validate_username(self, username):
        """
        Validate username as either email or regular username and fetch the user.
        """
        try:
            user, _ = User.get_by_identifier(username)
        except ValueError as e:
            raise serializers.ValidationError(str(e)) 

        # Ensure the user is active
        if not user.is_active:
            raise ValidationError(_("User account is deactivated."))
        return user.username  

    def get_token(self, user):
        """
        Generate a JWT token with custom user data and token lifetime.
        """
        token = super().get_token(user)

        # Add custom claims
        token['permissions'] = [str(permission) for permission in user.get_all_permissions()]
        token['email'] = user.email
        token['id'] = user.id

        # Adjust token lifetime if "remember_me" is true
        if self.initial_data.get('remember_me'):
            self.access_token_lifetime = timezone.timedelta(minutes=21600)

        # Set custom token lifetime
        setattr(token.access_token_class, 'lifetime', self.access_token_lifetime)
        return token

class CustomTokenRefreshSerializer(TokenRefreshSerializer):

    def __init__(self, *args, **kwargs):
        super(CustomTokenRefreshSerializer, self).__init__(*args, **kwargs)
        self.access_token_lifetime = timezone.timedelta(minutes=30)  # Default access token lifetime

    def validate(self, attrs):
        if self.initial_data.get('remember_me'):
            self.access_token_lifetime = timezone.timedelta(minutes=21600)

        # overriding access token lifetime
        setattr(self.token_class.access_token_class, 'lifetime', self.access_token_lifetime)
        data = super(CustomTokenRefreshSerializer, self).validate(attrs)
        return data

class ForgotPasswordSerializer(serializers.Serializer):
    username = serializers.CharField() 

    def send_otp(self):
        username = self.validated_data['username']
        try:
            user, _ = User.get_by_identifier(username)
        except ValueError as e:
            raise serializers.ValidationError(str(e)) 

        # Generate OTP for password reset
        raw_otp = user.create_otp(purpose=OTP.PurposeChoices.RESET_PASSWORD)

        # Send Raw OTP via Email (and mobile if needed)


class ResetPasswordSerializer(serializers.Serializer):
    username = serializers.CharField()  # Can be email or mobile
    otp_code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        otp_code = data.get('otp_code')
        try:
            user, _ = User.get_by_identifier(username)
        except ValueError as e:
            raise serializers.ValidationError(str(e)) 

        # Validate the OTP
        user.validate_otp(otp_code, purpose=OTP.PurposeChoices.RESET_PASSWORD)
        return data

    def reset_password(self):
        username = self.validated_data['username']
        new_password = self.validated_data['new_password']

        # Find user by email or username
        user, _ = User.get_by_identifier(username)
        user.set_password(new_password)
        user.save()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        """Check if the old password is correct."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password":_("The old password is incorrect.")})
        return value

    def validate(self, data):
        """Ensure the new password matches the confirmation password."""
        new_password = data['new_password']
        confirm_password = data['confirm_password']

        if new_password != confirm_password:
            raise serializers.ValidationError("New password and confirm password do not match.")
        
        # Validate the new password using Django's built-in password validators
        try:
            validate_password(new_password)
        except ValidationError as e:
            raise serializers.ValidationError({"new_password": e.messages})

        return data

    def save(self, user, **kwargs):
        """Perform the password change by setting the new password."""
        new_password = self.validated_data['new_password']
        
        # Update the user's password
        user.set_password(new_password)
        user.save()
        return user

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate_refresh_token(self, value):
        """
        Validate the provided refresh token.
        Raise a ValidationError if the token is invalid or expired.
        """
        try:
            token = RefreshToken(value)  # Create a RefreshToken instance
        except Exception as e:
            raise ValidationError(f"Invalid refresh token: {str(e)}")
        return value

    def blacklist_token(self):
        """
        Blacklist the provided refresh token.
        """
        refresh_token = self.validated_data['refresh_token']
        token = RefreshToken(refresh_token)
        token.blacklist()