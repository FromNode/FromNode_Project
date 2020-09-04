from django.db import models
from django.contrib.auth.models import User

class Projects(models.Model):
    Code = models.CharField(max_length=255,default=0, unique=True)
    name = models.CharField(max_length=255)
    whoIsOwner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)