from django.urls import path
from .views import RegisterAPIView, LoginAPIView, LogoutAPIView, ChangePasswordAPIView
urlpatterns = [
    path('api/register/', RegisterAPIView.as_view(), name='api_register'),
    path('api/login/', LoginAPIView.as_view(), name='api_login'),
    path('api/logout/', LogoutAPIView.as_view(), name='api_logout'),
    path('api/change-password/', ChangePasswordAPIView.as_view(), name='api_change_password'),
]
