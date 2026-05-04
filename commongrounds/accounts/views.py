from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import RegisterForm, ProfileUpdateForm
from .models import Profile
from django.shortcuts import render


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('accounts:login')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'registration/profile_update.html'
    slug_field = 'user__username'
    slug_url_kwarg = 'username'

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)
    def get_object(self):
        return self.request.user.profile

    def get_success_url(self):
            return reverse_lazy('home')

    def homepage(request):
        return render(request, "homepage.html")
