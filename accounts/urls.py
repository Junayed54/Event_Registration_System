from django.urls import path
from .views import HomeView, LoginView, LogoutView, RegisterView, EditProfileView, ChangePasswordView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
]