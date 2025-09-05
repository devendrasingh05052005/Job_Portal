# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/candidate/', views.candidate_signup, name='candidate_signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/candidate/', views.candidate_dashboard, name='candidate_dashboard'),
    path('dashboard/recruiter/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('recruiter/post-job/', views.post_job, name='post_job'),
    path('apply/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('recruiter/jobs/<int:job_id>/applications/', views.recruiter_job_applications, name='recruiter_job_applications'),
    path('recruiter/applications/<int:app_id>/shortlist/', views.shortlist_application, name='shortlist_application'),
    path('recruiter/applications/<int:app_id>/reject/', views.reject_application, name='reject_application'),
]