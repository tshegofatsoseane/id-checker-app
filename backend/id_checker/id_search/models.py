from django.db import models

class IDRecord(models.Model):
    id_number =  models.CharField(max_length=13, unique=True)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    sa_citizen = models.BooleanField(default=True)
    search_count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.id_number


class PublicHoliday(models.Model):
    id_record = models.ForeignKey(IDRecord, on_delete=models.CASCADE, related_name='holidays')
    holiday_name = models.CharField(max_length=255)
    description = models.TextField()
    holiday_date = models.DateField()
    holiday_type = models.CharField(max_length=50)

    def __str__(self):
        return self.holiday_name