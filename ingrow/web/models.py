from django.db import models

# Create your models here.
class customers(models.Model):
    national_id = models.CharField(max_length = 256, primary_key = True)
    name = models.CharField(max_length = 256)
    phone_number = models.CharField(max_length = 256)
    address = models.CharField(max_length = 256)