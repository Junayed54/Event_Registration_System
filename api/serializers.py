from rest_framework import serializers
from django.contrib.auth.models import User
from events.models import Event
# Submission

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}



class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        
        
# class SubmissionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Submission
#         fields = ['id', 'participant', 'event', 'details']
#         read_only_fields = ['id']

#     def validate_event(self, value):
#         # Add any additional validation for the event field if needed
#         # For example, you might want to check if the event is open for submissions
#         # or if the participant is registered for the event.
#         return value