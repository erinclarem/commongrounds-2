from django.urls import path, include
from .views import ProfileUpdateView, RegisterView

app_name = 'accounts'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),  
    path('register/', RegisterView.as_view(), name='register'),
    path(
        '<str:username>/',
        ProfileUpdateView.as_view(),
        name='profile_update'
    ),
]
