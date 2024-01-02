# forms.py
from django import forms
from .models import Event
# Submission

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'location_name', 'available_slots', 'registration_deadline']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'registration_deadline': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = []

# class SubmissionForm(forms.ModelForm):
#     class Meta:
#         model = Submission
#         fields = ['details']
#         widgets = {
#             'details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#         }



class EventSearchForm(forms.Form):
    search_query = forms.CharField(label='Search Events', max_length=100)