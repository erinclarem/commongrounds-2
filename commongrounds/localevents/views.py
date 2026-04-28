from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from .models import Event, EventType, EventSignup
# Create your views here.


class LocalEventsListView(ListView):
    model = Event
    template_name = "localevents_list.html"
    context_object_name = 'events'


class LocalEventDetailView(DetailView):
    model = Event
    template_name = "localevent_detail.html"

class LocalEventAddView(CreateView):
    model = Event
    template_name = "localevent_form.html"
    fields = ['title', 'category', 'organizers', 'event_image', 'description', 'location', 'start_time', 'end_time', 'event_capacity']

class LocalEventEditView(UpdateView):
    model = Event
    template_name = "localevent_form.html"
    fields = ['title', 'category', 'organizers', 'event_image', 'description', 'location', 'start_time', 'end_time', 'event_capacity']

class LocalEventSignupView(CreateView):
    model = EventSignup
    template_name = "localevent_signup_form.html"
    fields = ['Event', 'User_Registrant', 'New_Registrant']
