from django.contrib import admin
from .models import Event, EventType
# Register your models here.


class EventTypeAdmin(admin.ModelAdmin):
    model = EventType


class EventAdmin(admin.ModelAdmin):
    model = Event
    search_fields = ['title', 'location']
    list_display = ['title', 'category', 'location', 'start_time', 'end_time']
    list_filter = ['category', 'start_time', 'end_time']


admin.site.register(Event, EventAdmin)
admin.site.register(EventType, EventTypeAdmin)
