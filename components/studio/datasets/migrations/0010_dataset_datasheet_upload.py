# Generated by Django 2.2.13 on 2020-12-14 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0009_auto_20201214_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='datasheet_upload',
            field=models.FileField(default=None, upload_to='datasheets/'),
        ),
    ]
