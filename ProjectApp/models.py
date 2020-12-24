from django.db import models
from django.contrib.auth.models import User
from random import choice
from datetime import datetime
import string

def random_code():
    arr = [choice(string.ascii_letters) for _ in range(8)]
    Code = ''.join(arr)
    return Code

class Projects(models.Model):
    objects = models.Manager()
    Code = models.CharField(max_length=255,default=random_code, unique=True)
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField(default = datetime.now, blank = True, null=True)
    due_date = models.DateTimeField(blank = True, null=True)
    description = models.TextField(max_length= 20000, blank = True)
    members = models.ManyToManyField(User,blank = True)
    likeornot = models.BooleanField(default=False)
    def __str__(self):
        return self.name