from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate

from chatbot.models import MedicalReport
from chatbot.serializers import MedicalReportSerializer



@api_view(['POST'])
def upload_medical_report(request):
    try:
        files = request.FILES.getlist('file')
        if not files:
            return Response({'detail': 'No files uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MedicalReportSerializer(data=[
            {'user': request.user.id, 'report': file} for file in files
        ], many=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Files uploaded successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)