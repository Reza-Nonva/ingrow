# Generated by Django 5.0 on 2024-01-05 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_remove_person_birth_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Person',
        ),
    ]
