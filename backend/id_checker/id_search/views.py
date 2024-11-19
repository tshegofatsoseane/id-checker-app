from django.shortcuts import render

import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import IDRecord, PublicHoliday
from .serializers import IDRecordSerializer, PublicHolidaySerializer

@api_view(['POST'])
def id_search(request):
    id_number = request.data.get('idNumber')

    if len(id_number) != 13:
        return Response({'error': 'Invalid Id number'}, status=status.HTTP_400_BAD_REQUEST)
    
