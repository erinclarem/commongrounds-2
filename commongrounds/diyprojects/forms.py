from django import forms
from .models import Project, ProjectRating, ProjectReview


class ProjectRatingForm (forms.ModelForm):
    class Meta:
        model = ProjectRating
        fields = ['score']


class ProjectReviewForm (forms.ModelForm):
    class Meta:
        model = ProjectReview
        fields = ['comment', 'image']


class ProjectForm (forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'category', 'description', 'materials','steps']
        

class ProjectUpdateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'category', 'description', 'materials', 'steps']
