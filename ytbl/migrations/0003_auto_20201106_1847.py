# Generated by Django 3.1.2 on 2020-11-06 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ytbl', '0002_coordinates_type_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coordinates',
            name='lot_number',
            field=models.CharField(max_length=100),
        ),
    ]
