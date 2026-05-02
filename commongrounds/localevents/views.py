from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.mixins import RoleRequiredMixin
from .models import Event, EventType, EventSignup
from .forms import EventForm, EventSignupForm
from django.urls import reverse


class LocalEventsListView(ListView):
    model = Event
    template_name = "localevents_list.html"
    context_object_name = 'events'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            profile = self.request.user.profile

            context['created_events'] = Event.objects.filter(
                organizers=profile)
            context['signed_events'] = Event.objects.filter(
                event_signups__user_registrant=profile)
            context['other_events'] = Event.objects.exclude(
                organizers=profile
            ).exclude(
                event_signups__user_registrant=profile
            )
        else:
            context['other_events'] = Event.objects.all()

        return context


class LocalEventDetailView(DetailView):
    model = Event
    template_name = "localevent_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object
        is_owner = False
        is_full = event.event_signups.count() >= event.event_capacity

        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            is_owner = event.organizers.filter(id=profile.id).exists()

        can_signup = not is_full and not is_owner

        context['can_signup'] = can_signup
        context['is_owner'] = is_owner
        context['is_full'] = is_full

        return context


class LocalEventAddView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Event
    template_name = "localevent_form.html"
    form_class = EventForm  
    required_role = "Event Organizer"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.organizers.add(self.request.user.profile)
        return response
    def get_success_url(self):
        return reverse('localevents:detail', kwargs={'pk': self.object.pk})


class LocalEventEditView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Event
    template_name = "localevent_form.html"
    form_class = EventForm
    required_role = "Event Organizer"

    def form_valid(self, form):
        response = super().form_valid(form)

        if self.object.event_signups.count() >= self.object.event_capacity:
            self.object.status = 'Full'
        else:
            self.object.status = 'Available'

        self.object.save()
        return response
    def get_success_url(self):
        return reverse('localevents:detail', kwargs={'pk': self.object.pk})


class LocalEventSignupView(LoginRequiredMixin, CreateView):
    model = EventSignup
    template_name = "localevent_signup.html"
    form_class = EventSignupForm

    def form_valid(self, form):
        event = Event.objects.get(id=self.kwargs['pk'])
        form.instance.event = event
        if self.request.user.is_authenticated:
            form.instance.user_registrant = self.request.user.profile
            form.instance.new_registrant = None
        else:
            form.instance.user_registrant = None

        return super().form_valid(form)
