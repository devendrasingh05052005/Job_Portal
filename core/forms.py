from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Job, Application



class CandidateSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'is_candidate')



class JobPostingForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'is_internal', 'external_url', 'job_field']



class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume']
