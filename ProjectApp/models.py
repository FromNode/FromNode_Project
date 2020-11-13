from django.db import models
from django.contrib.auth.models import User
from random import choice
import string

def random_code():
    arr = [choice(string.ascii_letters) for _ in range(8)]
    Code = ''.join(arr)
    return Code

class Projects(models.Model):
    objects = models.Manager()
    Code = models.CharField(max_length=255,default=random_code, unique=True)
    name = models.CharField(max_length=255)
    whoIsOwner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)