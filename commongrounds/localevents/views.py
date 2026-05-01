from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.mixins import RoleRequiredMixin
from .models import Event, EventSignup
from .forms import EventForm, EventSignupForm


class LocalEventsListView(ListView):
    model = Event
    template_name = "localevents_list.html"
    context_object_name = 'events'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        if user.is_authenticated:
            profile = user.profile

            created_events = Event.objects.filter(organizers=profile)
            signed_events = Event.objects.filter(
                event_signups__user_registrant=profile)

            other_events = Event.objects.all()
            other_events = other_events.exclude(organizers=profile)
            other_events = other_events.exclude(
                event_signups__user_registrant=profile)

            context['created_events'] = created_events
            context['signed_events'] = signed_events
            context['other_events'] = other_events
        else:
            context['other_events'] = Event.objects.all()

        return context


class LocalEventDetailView(DetailView):
    model = Event
    template_name = "localevent_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        event = self.object
        user = self.request.user

        can_signup = True

        if user.is_authenticated:
            profile = user.profile

            if event.organizers.filter(id=profile.id).exists():
                can_signup = False

        if event.event_signups.count() >= event.event_capacity:
            can_signup = False

        context['can_signup'] = can_signup
        return context


class LocalEventAddView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Event
    template_name = "localevent_form.html"
    form_class = EventForm
    required_role = "Event Organizer"

    def form_valid(self, form):
        response = super().form_valid(form)

        profile = self.request.user.profile
        self.object.organizers.add(profile)

        return response


class LocalEventEditView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Event
    template_name = "localevent_form.html"
    form_class = EventForm
    required_role = "Event Organizer"

    def form_valid(self, form):
        response = super().form_valid(form)

        signup_count = self.object.event_signups.count()
        capacity = self.object.event_capacity

        if signup_count >= capacity:
            self.object.status = 'Full'
        else:
            self.object.status = 'Available'

        self.object.save()

        return response


class LocalEventSignupView(CreateView):
    model = EventSignup
    template_name = "localevent_signup_form.html"
    form_class = EventSignupForm

    def form_valid(self, form):
        event_id = self.kwargs['pk']
        event = Event.objects.get(id=event_id)

        form.instance.event = event

        user = self.request.user

        if user.is_authenticated:
            profile = user.profile
            form.instance.user_registrant = profile

        return super().form_valid(form)
