from django.db import models


class Register(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=15)
   #role = models.ForeignKey(Role, on_delete=models.CASCADE, default=2)  # Assuming 2 is the ID for the Editor role
    role = models.CharField(max_length=10, default='user')

    class Meta:
        db_table = "register"
        
class LOTP(models.Model):
    otpL = models.CharField(max_length=4, blank=True, null=True)
    username = models.CharField(max_length=100)

    class Meta:
        db_table="LOTP"

class Profile(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    email = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = "profile"

class Predict(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    N = models.IntegerField()
    temp = models.IntegerField()
    rainfall = models.FloatField()
    jathak = models.CharField(max_length=28)
    timesytamp = models.DateField()

    class Meta:
        db_table = "predict"
