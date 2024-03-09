from django.db import models


class admin(models.Model):
    mobile_no = models.CharField(max_length=10, unique=True, default=None)
    email = models.EmailField()
    password = models.CharField(max_length=8)

    class Meta:
        db_table = 'authentication_admin'

    def str(self):
        return self.mobile_no


class travel_agency(models.Model):
    agency_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile_no = models.CharField(max_length=10, unique=True, default=None)
    address = models.CharField(max_length=100)
    aadhar_no = models.CharField(max_length=13, unique=True)
    password = models.CharField(max_length=8)
    status = models.CharField(max_length=10, default=True)
    file = models.FileField(upload_to='file', default=True)

    class Meta:
        db_table = 'authentication_travel_agency'


class user(models.Model):
    user_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile_no = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=8)

    class Meta:
        db_table = 'authentication_user'


class Verified_travel_agency(models.Model):
    agency_name = models.CharField(max_length=100, default=None)
    email = models.EmailField(unique=True, default=None)
    mobile_no = models.CharField(max_length=10, unique=True, default=None)
    address = models.CharField(max_length=100, default=None)
    aadhar_no = models.CharField(max_length=13, unique=True, default=None)
    password = models.CharField(max_length=8, default=None)
    file = models.FileField(upload_to='file', default=True)

    class Meta:
        db_table = 'authentication_verified_travel_agency'


class schedule(models.Model):
    bus_type = models.CharField(max_length=30)
    form = models.CharField(max_length=30)
    to = models.CharField(max_length=30)
    total_seats = models.CharField(max_length=3)
    window = models.CharField(max_length=3)
    agency_number = models.CharField(max_length=10, default="")
    general = models.CharField(max_length=3)
    price = models.CharField(max_length=5)
    bus_number = models.CharField(max_length=10, default=None)
    date = models.DateField()
    agency_name = models.CharField(max_length=30, default="")
    time = models.TimeField()

    class meta:
        db_table = 'authentication_schedule'


class ticket(models.Model):
    ticketid = models.CharField(max_length=100)
    b_from = models.CharField(max_length=30)
    b_to = models.CharField(max_length=30)
    Customer_name = models.CharField(max_length=100, default=None)
    Agency_number = models.CharField(max_length=10)
    bus_type = models.CharField(max_length=30)
    Customer_number = models.CharField(max_length=10)
    date = models.CharField(max_length=60)
    Seats = models.CharField(max_length=3)
    amount = models.CharField(max_length=20)
    seat_type = models.CharField(max_length=10)
    Agency_name = models.CharField(max_length=100)
    bus_number = models.CharField(max_length=10)
    time = models.CharField(max_length=30)
    booking_time = models.TimeField()

    class meta:
        db_table = "authentication_ticket"
# Create your models here.