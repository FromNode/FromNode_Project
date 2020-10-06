from django.db import models
from django.contrib.auth.models import User

class Projects(models.Model):
<<<<<<< HEAD
    Code = models.CharField(max_length=255,default=0, unique=True)
=======
    Code = models.CharField(default=0, max_length=255, unique=True)
>>>>>>> 93ec2910d097ff6e53e6d82d94a529fc169e862f
    name = models.CharField(max_length=255)
    whoIsOwner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)