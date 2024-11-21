from rest_framework import serializers
from .models import IDRecord, PublicHoliday

class IDRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = IDRecord
        fields = ['id_number', 'gender', 'date_of_birth', 'sa_citizen', 'search_count']

class PublicHolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicHoliday
        fields = ['holiday_name', 'description', 'holiday_date', 'holiday_type']
