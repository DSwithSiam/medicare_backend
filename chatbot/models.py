from django.db import models
from accounts.models import CustomUser

class MedicalReport(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='medical_reports')
    report = models.FileField(upload_to='medical_reports/')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.user.email}"