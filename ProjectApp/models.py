from django.db import models
from NodeApp import models

class Projects(models.Model):
    ID = models.CharField(default=0, unique=True)
    name = models.CharField(max_length=255)
    whoIsOwner = models.ForeignKey(NodeApp.,on_delete=SET_NULL, null=True, blank=True)