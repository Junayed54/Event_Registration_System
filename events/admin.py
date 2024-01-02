from django.contrib import admin
from .models import Event, UserDashboard
# Submission

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'location_name', 'available_slots', 'user')
    search_fields = ['slug', 'title', 'location_name', 'user__username']
    prepopulated_fields = {'slug': ('title',)}

# admin.site.register(Submission)
admin.site.register(UserDashboard)