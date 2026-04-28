from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Event


class LocalEventsListView(ListView):
    model = Event
    template_name = "localevents_list.html"


class LocalEventDetailView(DetailView):
    model = Event
    template_name = "localevent_detail.html"
