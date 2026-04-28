from cProfile import Profile

from django.db import models
from django.urls import reverse

from commongrounds.commongrounds import settings


class EventType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Event(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        EventType,
        on_delete=models.SET_NULL,
        null=True,
        editable=False,
        related_name='events'
    )
    organizers = models.ManyToManyFiels(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name='organized_events'
        )
    event_image = models.ImageField(upload_to='event_images/')
    description = models.TextField()
    location = models.CharField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    event_capacity = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    status = models.CharField(
        max_length=20, 
        choices=(
            ('available', 'Available'),
            ('full', 'Full'),
            ('done', 'Done'),
            ('canceled', 'Canceled'),
            ), 
        default='available')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} at {self.location} from {self.start_time} to {self.end_time}"

    def get_absolute_url(self):
        return reverse('localevents:localevent_detail', args=[str(self.id)])

    class Meta:
        ordering = ['-created_on']

class EventSignup(models.Model):

    Event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='event_signups'
    )
    User_Registrant = models.ForeignKey(
        Profile,
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='event_signups'
    )
     
    New_Registrant = models.CharField()

# Create your models here.
