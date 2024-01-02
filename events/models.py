from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
import uuid

class Event(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location_name = models.CharField(max_length=255)
    available_slots = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events_created')
    participants = models.ManyToManyField(User, blank=True, related_name='events')
    registration_deadline = models.DateTimeField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date']
        



class UserDashboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dashboard')
    created_events = models.ManyToManyField('Event', related_name='created_by', blank=True)
    registered_events = models.ManyToManyField('Event', related_name='registered_users', blank=True)

    def __str__(self):
        return f"{self.user.username}'s Dashboard"        
        
# class Submission(models.Model):
#     participant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="submissions")
#     event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
#     details = models.TextField(null=True, blank=False)
#     id = models.UUIDField(default=uuid.uuid4, unique=True,
#                           primary_key=True, editable=False)

#     def __str__(self):
#         return f"{self.event} - {self.participant}"