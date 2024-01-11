# Generated by Django 5.0 on 2024-01-11 13:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0019_buy_buy_table_primary_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buy',
            name='project_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.projects'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='national_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.customers'),
        ),
        migrations.CreateModel(
            name='payments',
            fields=[
                ('payment_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('amout', models.BigIntegerField()),
                ('timestamp', models.DateTimeField()),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.projects')),
            ],
        ),
    ]