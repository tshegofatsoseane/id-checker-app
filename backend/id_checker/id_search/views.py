import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime
from .models import IDRecord, PublicHoliday
from .serializers import IDRecordSerializer, PublicHolidaySerializer
from django.conf import settings

def validator(id_number):
    """validate id no. using luhn algorithm"""
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

def decoder(id_number):
    """decode id no.and return its parts/components"""
    if len(id_number) != 13 or not id_number.isdigit():
        raise ValueError("Invalid ID number format")

    # extract parts/components from the id no.
    birth_str = id_number[:6] 
    gender_code = int(id_number[6:10])  
    citizenship = int(id_number[10]) 

    if not validator(id_number):
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
def search_id(request):
    
    id_no = request.data.get('idNumber')

    if len(id_no) != 13:
            return Response({'error': 'Invalid ID number'}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        decoded_info = decoder(id_no)

         # check if id exists in database and create new record
        record, created = IDRecord.objects.get_or_create(
            id_number=id_no,
            defaults=decoded_info
        )

        if not created:
            record.search_count += 1
            record.save()

        # fetch holidays using API
        response = requests.get('https://calendarific.com/api/v2/holidays', params={
            'api_key': settings.CALENDARIFIC_API_KEY,
            'country': 'ZA',
            'year': record.date_of_birth.year,
        })

        if response.status_code != 200:
            raise ValueError(f"Failed to fetch holidays: {response.status_code}")
            
        holidays = response.json().get('response', {}).get('holidays', [])
        matching_holidays = [
             holiday for holiday in holidays if holiday['date']['iso'] == str(record.date_of_birth)
        ]

        # store holidays in database
        for holiday in matching_holidays:
            PublicHoliday.objects.create(
                id_record=record,
                holiday_name=holiday['name'],
                description=holiday.get('description', ''),
                holiday_date=holiday['date']['iso'],
                holiday_type=holiday.get('type', ['General'])[0],
            )

        # return result 
        return Response({
            'idNumber': record.id_number,
            'dateOfBirth': record.date_of_birth,
            'gender': record.gender,
            'saCitizen': record.sa_citizen,
            'searchCount': record.search_count,
            'holidays': PublicHolidaySerializer(record.holidays.all(), many=True).data
            })

    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)