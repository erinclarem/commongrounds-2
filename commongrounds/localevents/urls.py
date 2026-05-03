from django.urls import path
from .views import LocalEventsListView, LocalEventDetailView, LocalEventAddView, LocalEventEditView, LocalEventSignupView

urlpatterns = [
    path('events/', LocalEventsListView.as_view(), name='localevents_list'),
    path('event/<int:pk>/',
         LocalEventDetailView.as_view(), name='localevent_detail'),
    path('event/add/', LocalEventAddView.as_view(), name='localevent_add'),
    path('event/<int:pk>/edit/',
         LocalEventEditView.as_view(), name='localevent_edit'),
    path('event/<int:pk>/signup/',
         LocalEventSignupView.as_view(), name='localevent_signup'),
]

app_name = 'localevents'
