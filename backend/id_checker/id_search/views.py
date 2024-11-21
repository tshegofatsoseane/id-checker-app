import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime

# Luhn algorithm
def validator(id_number):
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

def decoder(id_number):
    """decode iD number and return it's parts/components"""
    if len(id_number) != 13 or not id_number.isdigit():
        raise ValueError("Invalid ID number format")

     # extract parts/components from the id no.
    birth_str = id_number[:6] 
    gender_code = int(id_number[6:10])  
    citizenship = int(id_number[10]) 
    checksum = int(id_number[12])

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

@api_view(['POST', 'GET'])
def search_id(request):
        
        id_no = request.data.get('idNumber')

        if len(id_no) != 13:
            return Response({'error': 'Invalid ID number'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # decode id number
            decoded_info = decoder(id_no)

            # fetch holidays using calendarific API
            response = requests.get('https://calendarific.com/api/v2/holidays', params={
                'api_key': 'AdaT3t4fsQjgafmF7pNB7sItlvTaDVU3',
                'country': 'ZA',
                'year': decoded_info['date_of_birth'].year,
            })

            if response.status_code != 200:
                raise ValueError(f"Failed to fetch holidays: {response.status_code}")

            holidays = response.json().get('response', {}).get('holidays', [])

            matching_holidays = [
                {
                    'holidayName': holiday['name'],
                    'description': holiday.get('description', ''),
                    'holidayDate': holiday['date']['iso'],
                    'holidayType': holiday['type'][0] if 'type' in holiday else 'General',
                }
                for holiday in holidays if holiday['date']['iso'] == str(decoded_info['date_of_birth'])
            ]

            # return results
            return Response({
                'idNumber': id_no,
                'dateOfBirth': decoded_info['date_of_birth'],
                'gender': decoded_info['gender'],
                'saCitizen': decoded_info['sa_citizen'],
                'holidays': matching_holidays
            })

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
