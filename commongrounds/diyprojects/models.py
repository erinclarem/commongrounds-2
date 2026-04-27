from django.db import models
from django.urls import reverse
from accounts.models import Profile
from django.core.validators import MinValueValidator, MaxValueValidator


class ProjectCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('diyprojects:project_category', args=[str(self.id)])

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['name']


class Project(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='projects',
    )
    creator = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name='projects',
    )
    description = models.TextField()
    materials = models.TextField()
    steps = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('diyprojects:project_detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'project'
        verbose_name_plural = 'projects'
        ordering = ['-created_on']


class Favorite(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    date_favorited = models.DateTimeField()
    STATUS_CHOICES = [
        ('backlog', 'Backlog'),
        ('todo', 'To-Do'),
        ('done', 'Done'),
    ]
    project_status = models.CharField(
        max_length=7,
        choices=STATUS_CHOICES,
        default='backlog',
    )


class ProjectReview(models.Model):
    reviewer = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    comment = models.TextField()
    image = models.ImageField(
        upload_to='images/',
        null=True,
        blank=True
    )


class ProjectRating(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='ratings',
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
        )
