from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.mixins import RoleRequiredMixin
from .models import Event, EventType, EventSignup
from .forms import EventForm, EventSignupForm
from django.shortcuts import redirect


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
            other_events = Event.objects.exclude(
                organizers=profile
            ).exclude(
                event_signups__user_registrant=profile
            )

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
        is_owner = False
        is_full = event.event_signups.count() >= event.event_capacity
        can_signup = True

        if user.is_authenticated:
            profile = user.profile
            if event.organizers.filter(id=profile.id).exists():
                can_signup = False
                is_owner = True

        if is_full:
            can_signup = False

        context['can_signup'] = can_signup
        context['is_owner'] = is_owner
        context['is_full'] = is_full

        return context

class LocalEventAddView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Event
    template_name = "localevent_form.html"
    form_class = EventForm
    required_role = "Event Organizer" #check with accounts app to check if this is the name

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.organizers.add(self.request.user.profile)
        return response


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


class LocalEventSignupView(CreateView):
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
            return redirect('accounts:login')

        return super().form_valid(form)