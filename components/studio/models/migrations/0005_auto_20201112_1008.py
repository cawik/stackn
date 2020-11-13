# Generated by Django 2.2.13 on 2020-11-12 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0004_modellog_endpoint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modellog',
            name='current_git_commit',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='modellog',
            name='current_git_repo',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='modellog',
            name='endpoint',
            field=models.CharField(blank=True, default='', max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='modellog',
            name='trained_model',
            field=models.CharField(default='', max_length=32),
        ),
        migrations.AlterField(
            model_name='modellog',
            name='training_duration',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='modellog',
            name='training_started_at',
            field=models.CharField(max_length=255),
        ),
    ]