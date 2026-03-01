from django.urls import path
from .views import LocalEventsListView, LocalEventsDetailView
urlpatterns = [
    path('localevents/list', LocalEventsListView.as_view(), name='local_events_list'),
    path('localevents/event/<int:pk>/', LocalEventsDetailView.as_view(), name='local_event_detail'),
    ]

app_name = 'localevents'