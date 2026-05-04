from pyexpat.errors import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.mixins import RoleRequiredMixin
from .models import Event, EventType, EventSignup
from .forms import EventForm, EventSignupForm
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib import messages


class LocalEventsListView(ListView):
    model = Event
    template_name = "localevents_list.html"

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
        is_owner = False
        is_full = self.object.event_signups.count() >= self.object.event_capacity

        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            is_owner = self.object.organizers.filter(id=profile.id).exists()

        context['can_signup'] = not is_full and not is_owner
        context['is_owner'] = is_owner
        context['is_full'] = is_full
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not request.user.is_authenticated:
            return redirect('localevents:localevent_signupform', pk=self.object.pk)

        if self.object.organizers.filter(id=request.user.profile.id).exists():
            return redirect(self.object.get_absolute_url())

        if self.object.event_signups.count() >= self.object.event_capacity:
            self.object.status = 'full'
            self.object.save()
            messages.error(request, "Event is full.")
            return redirect('localevents:localevents_list')

        EventSignup.objects.create(
            event=self.object,
            user_registrant=request.user.profile
        )
        self.object.update_status()
        messages.success(request, "Signup successful!")
        return redirect('localevents:localevents_list')


class LocalEventAddView(RoleRequiredMixin, LoginRequiredMixin, CreateView):
    model = Event
    template_name = "localevent_form.html"
    form_class = EventForm
    required_role = "Event Organizer"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.organizers.add(self.request.user.profile)
        return response

    def get_success_url(self):
        return reverse('localevents:localevent_detail', kwargs={'pk': self.object.pk})


class LocalEventUpdateView(RoleRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Event
    template_name = "localevent_form.html"
    form_class = EventForm
    required_role = "Event Organizer"

    def form_valid(self, form):
        response = super().form_valid(form)

        self.object.save()
        return response

    def get_success_url(self):
        return reverse('localevents:localevent_detail', kwargs={'pk': self.object.pk})


class LocalEventSignupForm(CreateView):
    model = EventSignup
    template_name = "localevent_signupform.html"
    form_class = EventSignupForm

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = Event.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.event = Event.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('localevents:localevent_detail', kwargs={'pk': self.kwargs['pk']})
