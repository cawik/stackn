# Generated by Django 2.2.13 on 2020-12-14 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0011_auto_20201214_1602'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='datasheet_upload',
        ),
    ]
