from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from accounts.models import Profile


class EventType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        EventType,
        on_delete=models.SET_NULL,
        null=True,
        related_name='events'
    )
    organizers = models.ManyToManyField(
        Profile,
        related_name='organized_events',
        blank=True

    )
    event_image = models.ImageField(upload_to='event_images/')
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    event_capacity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)])
    status = models.CharField(
        max_length=10,
        choices=[
            ('Available', 'Available'),
            ('Full', 'Full'),
            ('Done', 'Done'),
            ('Cancelled', 'Cancelled'),
        ],
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def get_absolute_url(self):
        return reverse(
            'localevents:localevent_detail',
            args=[self.id]
        )


class EventSignup(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='event_signups'
    )
    user_registrant = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='event_signups'
    )
    new_registrant = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
