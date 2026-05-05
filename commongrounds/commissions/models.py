from django.db import models
from django.urls import reverse
from accounts.models import Profile
 
 
class CommissionType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
 
    class Meta:
        ordering = ['name']
 
    def __str__(self):
        return self.name
 
 
class Commission(models.Model):
    STATUS_OPEN = 'Open'
    STATUS_FULL = 'Full'
    STATUS_CHOICES = [
        (STATUS_OPEN, 'Open'),
        (STATUS_FULL, 'Full'),
    ]
 
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.ForeignKey(
        CommissionType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    maker = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='commissions_made',
    )
    people_required = models.PositiveIntegerField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN,
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
 
    class Meta:
        ordering = ['created_on']
 
    def __str__(self):
        return self.title
 
    def get_absolute_url(self):
        return reverse('commissions:detail', args=[str(self.pk)])
 
 
class Job(models.Model):
    STATUS_OPEN = 'Open'
    STATUS_FULL = 'Full'
    STATUS_CHOICES = [
        (STATUS_OPEN, 'Open'),
        (STATUS_FULL, 'Full'),
    ]
 
    commission = models.ForeignKey(
        Commission,
        on_delete=models.CASCADE,
        related_name='jobs',
    )
    role = models.CharField(max_length=255)
    manpower_required = models.PositiveIntegerField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN,
    )
 
    class Meta:
        ordering = ['status', '-manpower_required', 'role']
 
    def __str__(self):
        return f'{self.role} ({self.commission.title})'
 
    def accepted_count(self):
        return self.applications.filter(status=JobApplication.STATUS_ACCEPTED).count()
 
    def is_full(self):
        return self.accepted_count() >= self.manpower_required
 
 
class JobApplication(models.Model):
    STATUS_PENDING = 'Pending'
    STATUS_ACCEPTED = 'Accepted'
    STATUS_REJECTED = 'Rejected'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_REJECTED, 'Rejected'),
    ]
 
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications',
    )
    applicant = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='job_applications',
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    applied_on = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        ordering = [
            models.Case(
                models.When(status='Pending', then=0),
                models.When(status='Accepted', then=1),
                models.When(status='Rejected', then=2),
                default=3,
                output_field=models.IntegerField(),
            ),
            '-applied_on',
        ]
 
    def __str__(self):
        return f'{self.applicant} → {self.job.role}'
