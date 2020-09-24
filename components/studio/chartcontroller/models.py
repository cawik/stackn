from django.db import models

# Create your models here.
class ChartResource(models.Model):
    name = models.CharField(max_length=512, unique=True)
    namespace = models.CharField(max_length=512)
    chart = models.CharField(max_length=512)
    params = models.CharField(max_length=10000)
    username = models.CharField(max_length=512)
    status = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)