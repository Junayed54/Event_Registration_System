from django.urls import path
from .views import (
    EventCreateView,
    EventListView,
    EventDetailView,
    EventRegistrationView,
    # SubmissionCreateView,
    UserDashboardView,
    UnregisterFromEventView,
    ConfirmationPageView,
    EventUpdateView,
    EventDeleteView,
    EventSearchView
)

urlpatterns = [
    path('create/', EventCreateView.as_view(), name='event_create'),
    path('list/', EventListView.as_view(), name='event_list'),
    path('dashboard/', UserDashboardView.as_view(), name='user_dashboard'),
    path('<str:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('<slug:slug>/update/', EventUpdateView.as_view(), name='event_update'),
    path('<slug:slug>/delete/', EventDeleteView.as_view(), name='event_delete'),
    path('<str:pk>/register/', EventRegistrationView.as_view(), name='event_registration'),
    path('<str:pk>/unregister/', UnregisterFromEventView.as_view(), name='unregister_from_event'),
    path('confirmation/<str:pk>/', ConfirmationPageView.as_view(), name='confirmation_page'),
    # path('<str:pk>/submit/', SubmissionCreateView.as_view(), name='submission_create'),
    path('event/search/', EventSearchView.as_view(), name='event_search'),
    
]
