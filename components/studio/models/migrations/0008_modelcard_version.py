# Generated by Django 2.2.13 on 2020-12-21 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0007_auto_20201221_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelcard',
            name='version',
            field=models.IntegerField(default=1),
        ),
    ]