from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Profile


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['display_name']  # only editable field
    template_name = 'accounts/profile_update.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy('accounts:profile_update', kwargs={
            'username': self.request.user.username
        })
