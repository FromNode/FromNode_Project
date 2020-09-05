from django.db import models
from django.contrib.auth.models import User

class Projects(models.Model):
    Code = models.CharField(default=0, max_length=255, unique=True)
    name = models.CharField(max_length=255)
    whoIsOwner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)