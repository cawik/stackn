# Generated by Django 2.2.13 on 2020-12-19 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0003_modelcard'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modelcard',
            name='model_card',
        ),
        migrations.AddField(
            model_name='modelcard',
            name='caveats_and_recommendations',
            field=models.TextField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='modelcard',
            name='ethical_consideration',
            field=models.TextField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='modelcard',
            name='factors',
            field=models.TextField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='modelcard',
            name='intended_uses',
            field=models.TextField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='modelcard',
            name='metrics',
            field=models.TextField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='modelcard',
            name='model_details',
            field=models.TextField(default='', max_length=1000),
        ),
    ]
