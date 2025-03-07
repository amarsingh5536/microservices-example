from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.decorators import action
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import (CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer,
    ForgotPasswordSerializer, ResetPasswordSerializer, ChangePasswordSerializer, LogoutSerializer)

class CustomObtainPairView(TokenObtainPairView):
    """
    Custom view for obtaining JWT tokens with additional user data and permissions.
    """
    permission_classes = (AllowAny,) 
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to issue JWT tokens and additional user data.
        """
        data = request.data  # Get the request data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)

class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom view to refresh access tokens with additional user data.
    """
    serializer_class = CustomTokenRefreshSerializer

class ResetPasswordViewSet(viewsets.GenericViewSet):
    """
    1. Forgot Password: Send OTP to email/mobile.
    2. Reset Password: Verify OTP and update password.
    """
    def get_serializer_class(self):
        if self.action == 'forgot_password':
            return ForgotPasswordSerializer
        elif self.action == 'reset_password':
            return ResetPasswordSerializer
        else:
            return ForgotPasswordSerializer

    @action(methods=['POST'], detail=False, permission_classes=[])
    def forgot_password(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.send_otp()
            return Response({"message": "OTP sent successfully."})
        return Response(serializer.errors, status=400)

    @action(methods=['POST'], detail=False, permission_classes=[])
    def reset_password(self, request):
        serialized = ResetPasswordSerializer(data=request.data)
        if serialized.is_valid(raise_exception=True):
            serialized.reset_password()
            return Response({'message': 'Password is successfully updated'}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class LogoutViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def create(self, request, *args, **kwargs):
        """
        Handle the logout by blacklisting the provided refresh token.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.blacklist_token()
                return Response({"message": "Successfully logged out."},status=status.HTTP_200_OK)
            except Exception as e:
                raise ValidationError(f"Error logging out: {str(e)}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)