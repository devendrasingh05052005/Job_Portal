# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CandidateSignUpForm
from django.contrib.auth.decorators import login_required
from .forms import CandidateSignUpForm, JobPostingForm, ApplicationForm # <-- Yahan ApplicationForm add karein
from .models import Job, Application, JobField
from django.contrib import messages
from .api import fetch_adzuna_jobs # Naya import
from django.db.models import Count
from .utils import get_resume_ranking # Naya import
import fitz # PyMuPDF
import requests
from django.db.models import Count, Q # <-- Yeh naya import hai


def candidate_signup(request):
    if request.method == 'POST':
        form = CandidateSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_candidate = True
            user.save()
            return redirect('login') # <-- यहां 'accounts:login' को 'login' से बदल दिया गया है
    else:
        form = CandidateSignUpForm()
    return render(request, 'core/signup.html', {'form': form})



@login_required
def dashboard(request):
    if request.user.is_candidate:
        return redirect('candidate_dashboard')
    elif request.user.is_recruiter:
        return redirect('recruiter_dashboard')
    else:
        # Agar koi role na ho, to home page par bhej dein
        return redirect('home')
    

@login_required
def candidate_dashboard(request):
    if not request.user.is_candidate:
        return redirect('dashboard')

    query = request.GET.get('query', '')
    location = request.GET.get('location', '')
    
    internal_jobs = Job.objects.filter(is_internal=True)
    external_jobs = []

    if query:
        try:
            # External jobs fetch karein
            external_jobs_data = fetch_adzuna_jobs(query, location)
            for job_data in external_jobs_data:
                external_jobs.append({
                    'title': job_data['title'],
                    'description': job_data['description'],
                    'external_url': job_data['redirect_url']
                })
        except requests.exceptions.RequestException as e:
            # Agar API call fail ho to page par error dikhayein
            messages.error(request, f"API call failed. Please check your internet connection or API credentials.")
            print(f"API call failed with error: {e}") # Isse console mein bhi error dikhega
    
    my_applications = Application.objects.filter(candidate=request.user)

    context = {
        'internal_jobs': internal_jobs,
        'external_jobs': external_jobs,
        'my_applications': my_applications,
        'query': query,
        'location': location,
    }
    return render(request, 'core/candidate_dashboard.html', context)


@login_required
def recruiter_dashboard(request):
    if not request.user.is_recruiter:
        return redirect('dashboard')
    
    recruiter_jobs = Job.objects.filter(recruiter=request.user)

    context = {
        'jobs': recruiter_jobs,
    }
    return render(request, 'core/recruiter_dashboard.html', context)


@login_required
def post_job(request):
    if not request.user.is_recruiter:
        return redirect('dashboard') # Agar user recruiter nahi hai, toh wapas bhej dein

    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            return redirect('recruiter_dashboard')
    else:
        form = JobPostingForm()

    return render(request, 'core/post_job.html', {'form': form})







@login_required
def apply_for_job(request, job_id):
    if not request.user.is_candidate:
        return redirect('dashboard')
        
    job = get_object_or_404(Job, id=job_id, is_internal=True)
    
    if Application.objects.filter(candidate=request.user, job=job).exists():
        messages.info(request, "Aap is job par pehle hi apply kar chuke hain.")
        return redirect('candidate_dashboard')

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            resume_file = request.FILES['resume']
            job_description = job.description
            
            # Ranking score calculate karein
            ranking_score = get_resume_ranking(resume_file, job_description)
            
            if ranking_score is None:
                messages.error(request, "Resume file read nahi ho payi. Kripya sahi format mein file upload karein.")
                return redirect('apply_for_job', job_id=job.id)

            application = form.save(commit=False)
            application.candidate = request.user
            application.job = job
            application.ranking_score = ranking_score
            application.save()
            
            messages.success(request, "Aapka application safal ho gaya hai!")
            return redirect('candidate_dashboard')
    else:
        form = ApplicationForm()
        
    return render(request, 'core/apply_for_job.html', {'form': form, 'job': job})

def home(request):
    return render(request, 'core/home.html')


@login_required
def recruiter_job_applications(request, job_id):
    if not request.user.is_recruiter:
        return redirect('dashboard')
    
    # Check karein ki job recruiter ne hi post ki hai
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)
    
    # Saari applications ko ranking score ke hisaab se sort karein
    applications = Application.objects.filter(job=job).order_by('-ranking_score')
    
    return render(request, 'core/recruiter_job_applications.html', {'job': job, 'applications': applications})



@login_required
def shortlist_application(request, app_id):
    if not request.user.is_recruiter:
        return redirect('dashboard')
    
    # Check karein ki application ussi recruiter ki job ke liye hai
    application = get_object_or_404(Application, id=app_id, job__recruiter=request.user)
    
    # Application ka status 'Shortlisted' mein update karein
    application.status = 'Shortlisted'
    application.save()
    
    messages.success(request, f"{application.candidate.username} has been shortlisted.")
    return redirect('recruiter_job_applications', job_id=application.job.id)

@login_required
def reject_application(request, app_id):
    if not request.user.is_recruiter:
        return redirect('dashboard')
    
    # Check karein ki application ussi recruiter ki job ke liye hai
    application = get_object_or_404(Application, id=app_id, job__recruiter=request.user)
    
    # Application ka status 'Rejected' mein update karein
    application.status = 'Rejected'
    application.save()
    
    messages.success(request, f"{application.candidate.username} has been rejected.")
    return redirect('recruiter_job_applications', job_id=application.job.id)