import string
from datetime import datetime
from random import choice

from django.contrib.auth.models import User
from django.db import models
from NodeApp.models import Nodes


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
    unliked_members = models.ManyToManyField(User,blank = True, related_name ='Joined_Unliked_Projects')
    liked_members = models.ManyToManyField(User,blank = True, related_name ='Joined_Liked_Projects')
    Proj_Nodes = models.ManyToManyField(Nodes,blank = True, related_name ='ProjNode')
    def __str__(self):
        return self.name
        

class proj_with_user(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    proj_id = models.ForeignKey(Projects, on_delete=models.CASCADE, db_column="proj_id")
