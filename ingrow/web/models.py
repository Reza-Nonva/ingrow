from django.db import models

# Create your models here.
class customers(models.Model):
    national_id = models.CharField(max_length = 256, primary_key = True)
    name = models.CharField(max_length = 256)
    phone_number = models.CharField(max_length = 256)
    address = models.CharField(max_length = 256)


class broadcasts(models.Model):
    """
    we don't define a Primary key, django automaticlly will create ID as a primary key
    https://docs.djangoproject.com/en/5.0/topics/db/models/#automatic-primary-key-fields
    """
     
    national_id = models.ForeignKey(customers, on_delete = models.CASCADE)
    text = models.CharField(max_length = 256)
    status = models.BooleanField()
    timestamp = models.DateTimeField()