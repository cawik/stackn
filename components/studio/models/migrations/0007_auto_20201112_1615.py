# Generated by Django 2.2.13 on 2020-11-12 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0006_auto_20201112_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modellog',
            name='trained_model',
            field=models.CharField(default='', max_length=32),
        ),
    ]