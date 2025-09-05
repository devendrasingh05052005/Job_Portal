# resume_builder/forms.py
from django import forms

class ResumeBuilderForm(forms.Form):
    full_name = forms.CharField(label='Full Name', max_length=100)
    email = forms.EmailField(label='Email')
    phone_number = forms.CharField(label='Phone Number', max_length=20, required=False)
    
    # AI ke liye input field
    target_job_title = forms.CharField(label='Target Job Title', max_length=100)
    
    work_experience = forms.CharField(
        label='Your Work Experience',
        widget=forms.Textarea,
        required=False
    )
    
    education = forms.CharField(
        label='Education',
        widget=forms.Textarea,
        required=False
    )
    
    skills = forms.CharField(
        label='Skills (e.g., Python, SQL, Django)',
        widget=forms.Textarea,
        required=False
    )