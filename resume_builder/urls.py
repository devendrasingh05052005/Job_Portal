# resume_builder/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.choose_template, name='choose_template'),
    path('<int:template_id>/', views.resume_builder, name='resume_builder'),
    path('download/', views.download_resume, name='download_resume'),
]