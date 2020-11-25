# Generated by Django 2.2.13 on 2020-11-25 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('run_id', models.CharField(max_length=32)),
                ('trained_model', models.CharField(default='', max_length=32)),
                ('project', models.CharField(default='', max_length=255)),
                ('training_started_at', models.CharField(max_length=255)),
                ('execution_time', models.CharField(default='', max_length=255)),
                ('code_version', models.CharField(default='', max_length=255)),
                ('current_git_repo', models.CharField(default='', max_length=255)),
                ('latest_git_commit', models.CharField(default='', max_length=255)),
                ('system_details', models.TextField(blank=True)),
                ('cpu_details', models.TextField(blank=True)),
                ('training_status', models.CharField(choices=[('ST', 'Started'), ('DO', 'Done'), ('FA', 'Failed')], default='ST', max_length=2)),
            ],
            options={
                'unique_together': {('run_id', 'trained_model')},
            },
        ),
        migrations.CreateModel(
            name='Metadata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('run_id', models.CharField(max_length=32)),
                ('trained_model', models.CharField(default='', max_length=32)),
                ('project', models.CharField(default='', max_length=255)),
                ('model_details', models.TextField(blank=True)),
                ('parameters', models.TextField(blank=True)),
                ('metrics', models.TextField(blank=True)),
            ],
            options={
                'unique_together': {('run_id', 'trained_model')},
            },
        ),
    ]
