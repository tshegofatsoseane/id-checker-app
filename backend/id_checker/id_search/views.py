import datetime
from django.shortcuts import render

import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import IDRecord, PublicHoliday
from .serializers import IDRecordSerializer, PublicHolidaySerializer


# Luhn algorithm
def luhn_validator(id_number):
    """validate id number using luhn algorithm"""
    total = 0
    reverse_digits = id_number[::-1]
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1: 
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0

def decode_id_number(id_number):
    """decode iD number and return it's parts/components"""
    if len(id_number) != 13 or not id_number.isdigit():
        raise ValueError("Invalid ID number format")

    # extract parts/components from the id no.
    birth_str = id_number[:6] 
    gender_code = int(id_number[6:10])  
    citizenship = int(id_number[10]) 
    checksum = int(id_number[12])

    if not luhn_validator(id_number):
        raise ValueError("Invalid ID number checksum")

    birth_date = datetime.strptime(birth_str, '%y%m%d').date()

    if gender_code >= 5000:
        gender = "Male"
    else:
        gender = "Female"

     
    if citizenship == 0:
        citizen = True
    else:
        citizen = False

    return {
        'date_of_birth': birth_date,
        'gender': gender,
        'sa_citizen': citizen
    }


@api_view(['POST'])
def id_search(request):
    id_no = request.data.get('idNumber')

    if len(id_no) != 13:
        return Response({'error': 'Invalid Id number'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        decoded_info = decode_id_number(id_no)

        # check if id exist in database if not create new record
        record, created = IDRecord.objects.get_or_create(
            id_number=id_no,
            defaults=decoded_info
        )

        if not created:
            record.query_count += 1
            record.save()
    except:

