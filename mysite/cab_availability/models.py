from django.db import models


class CabDriver(models.Model):
    name = models.CharField(max_length=200,unique=True)
    car_number = models.CharField(max_length=200,unique=True)
    phone_number = models.CharField(max_length=13,unique=True)
    license_number = models.CharField(max_length=200,unique=True)
    email = models.CharField(max_length=200,unique=True)

    class Meta:
        db_table = 'cab_availability_cab_driver'


class CabPosition(models.Model):
    cab = models.ForeignKey(CabDriver, on_delete=models.CASCADE)
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)

    class Meta:
        db_table = 'cab_availability_cab_position'