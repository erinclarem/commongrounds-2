from django.urls import path
from .views import ProfileUpdateView

app_name = 'accounts'

urlpatterns = [
    path(
        '<str:username>/',
        ProfileUpdateView.as_view(),
        name='profile_update'
    ),
]
