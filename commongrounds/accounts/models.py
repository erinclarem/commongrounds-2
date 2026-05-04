from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
        if self.display_name:
            return f"{self.display_name}"
        return f"{self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
