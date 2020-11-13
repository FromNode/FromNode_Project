from django.db import models
from django.contrib.auth.models import User
from random import choice
import string


def random_code():
    _LENGTH = 8
    strings = ['1','2','3','4','5','6','7','8','9']
    string_pool = string.digits
    result = ''
    for i in range(_LENGTH):
        if i ==0:
            result+=choice(strings)
        result += choice(string_pool)
    return result

class Files(models.Model):
    fileName = models.CharField(max_length=1023)
    createdDate = models.DateTimeField(auto_now=True)
    Code = models.CharField(primary_key = True, max_length=255, default=random_code, unique=True)
    whoIsOwner = models.ForeignKey(User,on_delete = models.SET_NULL, null=True, blank=True)
    ownerPCode = models.ForeignKey('ProjectApp.projects', on_delete=models.CASCADE)
    image = models.CharField(max_length=255, default='etc')