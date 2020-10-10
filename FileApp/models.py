from django.db import models
from django.contrib.auth.models import User

class Files(models.Model):
    fileName = models.CharField(max_length=1023)
    createdDate = models.DateTimeField(auto_now=True)
    Code = models.CharField(primary_key = True, max_length=255, default=0, unique=True)
    whoIsOwner = models.ForeignKey(User,on_delete = models.SET_NULL, null=True, blank=True)
    ownerPCode = models.ForeignKey('ProjectApp.projects', on_delete=models.CASCADE)