from django.urls import path
from .views import LocalEventsListView, LocalEventDetailView, LocalEventAddView, LocalEventUpdateView, LocalEventSignupForm

urlpatterns = [
    path('events/', LocalEventsListView.as_view(), name='localevents_list'),
    path('event/<int:pk>/',
         LocalEventDetailView.as_view(), name='localevent_detail'),
    path('event/add/', LocalEventAddView.as_view(), name='localevent_add'),
    path('event/<int:pk>/edit/',
         LocalEventUpdateView.as_view(), name='localevent_edit'),
    path('event/<int:pk>/signup/',
         LocalEventSignupForm.as_view(), name='localevent_signupform'),
]

app_name = 'localevents'
