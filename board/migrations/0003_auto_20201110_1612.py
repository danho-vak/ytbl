# Generated by Django 3.1.2 on 2020-11-10 07:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_board_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='board',
            old_name='image',
            new_name='images',
        ),
    ]
