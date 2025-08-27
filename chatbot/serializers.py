
from .models import MedicalReport
from rest_framework import serializers


class MedicalReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalReport
        fields = ['user', 'report']