from django.db import models

# Create your models here.
class ModuleRegistry(models.Model):
    name = models.CharField(max_length=255, unique=True)
    installed = models.BooleanField(default=False)
    version = models.CharField(max_length=50, blank=True, null=True)