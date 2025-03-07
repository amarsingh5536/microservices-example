from django.urls import include, path
from rest_framework import routers
from .api import (CustomObtainPairView, CustomTokenRefreshView, ResetPasswordViewSet, ChangePasswordViewSet, LogoutViewSet)


router = routers.DefaultRouter()
router.register(r'', ResetPasswordViewSet, basename='reset-password')
router.register(r'change-password', ChangePasswordViewSet, basename='change-password')
router.register(r'logout', LogoutViewSet, basename='logout')


urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name="token_refresh"),
]


