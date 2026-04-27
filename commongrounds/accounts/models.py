from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    display_name = models.CharField(max_length=63)
    email = models.EmailField()
    ROLE_CHOICES = [
        ("Market Seller", "Market Seller"),
        ("Event Organizer", "Event Organizer"),
        ("Book Contributor", "Book Contributor"),
        ("Project Creator", "Project Creator"),
        ("Commission Maker", "Commission Maker"),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=True)


def __str__(self):
    return f"{self.display_name}"
