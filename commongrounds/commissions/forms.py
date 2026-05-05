from django import forms
from .models import Commission, Job


class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        exclude = ['maker']


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['role', 'manpower_required', 'status']


JobFormSet = inlineformset_factory(
    Commission,
    Job,
    form=JobForm,
    extra=1,
    can_delete=True
)

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = []