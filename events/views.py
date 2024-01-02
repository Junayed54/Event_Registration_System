from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, ListView, DetailView, FormView, UpdateView, DeleteView
# from django.db.models import Q
from .models import Event, UserDashboard
# Submission,
from .forms import EventRegistrationForm, EventForm, EventSearchForm
# SubmissionForm
from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    template_name = 'event_create.html'
    form_class = EventForm
    success_url = reverse_lazy('event_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EventListView(ListView):
    model = Event
    template_name = 'event_list.html'
    context_object_name = 'events'
    paginate_by = 5 

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Event.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        return Event.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(context['events'], self.paginate_by)
        page = self.request.GET.get('page')

        try:
            events = paginator.page(page)
        except PageNotAnInteger:
            events = paginator.page(1)
        except EmptyPage:
            events = paginator.page(paginator.num_pages)

        context['events'] = events
        return context


    
    
class UserDashboardView(LoginRequiredMixin, View):
    template_name = 'user_dashboard.html'

    def get(self, request):

        user_created_events = Event.objects.filter(user=request.user)

        user_registered_events = Event.objects.filter(participants=request.user)

        user_registered_events = user_registered_events.exclude(
            date__lt=timezone.now().date(),
            time__lt=timezone.now().time()
        )

        # Render the template with the events
        return render(request, self.template_name, {
            'user_created_events': user_created_events,
            'user_registered_events': user_registered_events,
        })

class EventDetailView(DetailView):
    model = Event
    template_name = 'event_detail.html'
    context_object_name = 'event'

    def  get_object(self):
        event_id = self.kwargs.get('pk')
        return get_object_or_404(Event, slug=event_id)
    

class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'event_update.html'
    slug_field = 'slug'
    success_url = reverse_lazy('event_list')


class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = 'event_delete.html'
    success_url = reverse_lazy('user_dashboard')
    slug_field = 'slug'
    
class EventRegistrationView(LoginRequiredMixin, FormView):
    template_name = 'event_registration.html'
    form_class = EventRegistrationForm

    def form_valid(self, form):
        event_id = self.kwargs['pk']
        event = get_object_or_404(Event, slug=event_id)

        if event.available_slots > event.participants.count() and timezone.now() < event.registration_deadline and not event.participants.filter(id=self.request.user.id).exists():
            event.available_slots -= 1
            event.save()

            event.participants.add(self.request.user)

            return redirect('event_list')
        else:
            return render(self.request, 'registration_failed.html')

# class SubmissionCreateView(LoginRequiredMixin, CreateView):
#     model = Submission
#     template_name = 'submission_create.html'
#     form_class = SubmissionForm
#     success_url = reverse_lazy('event_list')

#     def form_valid(self, form):
#         form.instance.participant = self.request.user
#         event_id = self.kwargs['pk']
#         form.instance.event = get_object_or_404(Event, id=event_id)
#         return super().form_valid(form)



class UnregisterFromEventView(LoginRequiredMixin, View):
    template_name = 'user_dashboard.html'

    def get(self, request, pk):
        event = get_object_or_404(Event, slug=pk)

        if event.date < timezone.now().date() or (event.date == timezone.now().date() and event.time < timezone.now().time()):
            return render(request, self.template_name, {'reason': 'Event has already taken place.'})

        if request.user in event.participants.all():
            return redirect('confirmation_page', pk=event.slug)
        else:
            return render(request, self.template_name, {'reason': 'User is not registered for this event.'})

    def post(self, request, pk):
        
        event = get_object_or_404(Event, slug=pk)
        print(event.title)
        if event.date < timezone.now().date() or (event.date == timezone.now().date() and event.time < timezone.now().time()):
            return render(request, self.template_name, {'reason': 'Event has already taken place.'})

        if request.user in event.participants.all():

            event.available_slots += 1
            

            event.participants.remove(request.user)
            event.save()
            
            return redirect('confirmation_page', pk=event.slug)
        else:
            return render(request, 'confirmation_page.html', {'reason': 'User is not registered for this event.'})
        
class ConfirmationPageView(LoginRequiredMixin, View):
    template_name = 'confirmation_page.html'
    def get(self, request, pk):
        event = get_object_or_404(Event, slug=pk)


        return render(request, self.template_name, {'event': event})
    
    
    
    
class EventSearchView(ListView):
    model = Event
    template_name = 'event_search_results.html'
    context_object_name = 'events'
    form_class = EventSearchForm

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search_query')

        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(self.request.GET)
        return context