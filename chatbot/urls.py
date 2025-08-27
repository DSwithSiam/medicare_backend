from django.urls import path
from .views import upload_medical_report

urlpatterns = [
    path('medical-report/upload/', upload_medical_report, name='upload_medical_report'),
]