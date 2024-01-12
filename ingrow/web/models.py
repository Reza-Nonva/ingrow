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

class products(models.Model):
    code = models.AutoField(primary_key=True)
    price = models.FloatField()
    order_point = models.IntegerField()
    status = models.BooleanField()              # True is procuct is avaiable else False
    name = models.CharField(max_length = 256)
    count = models.IntegerField()

class projects(models.Model):
    project_id = models.AutoField(primary_key=True)
    national_id = models.ForeignKey(customers, on_delete = models.CASCADE)
    description = models.CharField(max_length = 1024)

class buy(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.ForeignKey(products, on_delete = models.PROTECT)
    project_id = models.ForeignKey(projects, on_delete = models.CASCADE)
    timestamp = models.DateTimeField()
    count = models.IntegerField()
    price_per_unit = models.FloatField()
    total_price = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['id', 'code', 'project_id', 'timestamp'], name='buy_table_primary_key'
            )
        ]


class payments(models.Model):
    payment_id = models.BigIntegerField(primary_key = True)
    project_id = models.ForeignKey(projects, on_delete = models.CASCADE)
    amount = models.BigIntegerField()
    timestamp = models.DateTimeField()

class services(models.Model):
    code = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 256)
    price_per_unit = models.FloatField()

class works(models.Model):
    work_id = models.AutoField(primary_key=True)
    project_id = models.ForeignKey(projects, on_delete = models.CASCADE)
    timestamp = models.DateTimeField()

class work_report(models.Model):
    id = models.AutoField(primary_key=True)
    work_id = models.ForeignKey(works, on_delete = models.CASCADE)
    service_code = models.ForeignKey(services, on_delete = models.PROTECT)
    unit = models.FloatField()
    price_per_unit = models.FloatField()
    total_price = models.FloatField()

