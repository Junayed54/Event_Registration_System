from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, RedirectView, UpdateView
from .forms import SignUpForm, EditProfileForm, LoginForm
from django.contrib.auth.models import User



class HomeView(TemplateView):
    template_name = 'home.html'


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm  # Use the LoginForm instead of AuthenticationForm

    def form_valid(self, form):
        # The user is already authenticated by the form if valid
        login(self.request, form.get_user())
        messages.success(self.request, 'You\'re logged in')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')

class LogoutView(RedirectView):
    url = reverse_lazy('base')

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'You\'re now logged out')
        return super().get(request, *args, **kwargs)

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = SignUpForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        messages.success(self.request, 'You\'re now registered')
        return super().form_valid(form)

class EditProfileView(UpdateView):
    template_name = 'edit_profile.html'
    form_class = EditProfileForm
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user

class ChangePasswordView(FormView):
    template_name = 'change_password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the current user to the form
        return kwargs

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            update_session_auth_hash(self.request, self.request.user)
            messages.success(self.request, 'You have changed your password successfully.')
        return super().form_valid(form)