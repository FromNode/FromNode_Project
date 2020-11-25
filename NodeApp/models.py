from django.db import models
from django.contrib.auth.models import User
from random import choice
import string

def random_code():
    _LENGTH = 8
    string_pool = string.digits
    result = ''
    for i in range(_LENGTH):
        result += choice(string_pool)
    return result

class Nodes(models.Model):
    objects = models.Manager()
    Code = models.CharField(primary_key = True, max_length=255, default=random_code, unique=True) #노드별 고유 코드
    createdDate = models.DateTimeField(auto_now=True)
    fileObj = models.FileField(upload_to="media", blank=False) #이 노드에 저장되어 있는 파일
    previousCode = models.ForeignKey('self',on_delete=models.SET_NULL, null=True, blank=True) #이전 노드
    ownerPCode = models.ForeignKey('ProjectApp.projects', on_delete=models.CASCADE)#이 노드가 속해 있는 프로젝트
    ownerFCode = models.ForeignKey('FileApp.Files', on_delete=models.CASCADE)#이 노드가 속해 있는 프로젝트
    whoIsOwner = models.ForeignKey(User,on_delete = models.SET_NULL, null=True, blank=True)#이 노드를 만든 회원
    comment = models.CharField(max_length=200, blank = True, null=True)
    nodeName = models.CharField(max_length=100, blank = True, null=True)
    description = models.TextField(max_length=20000, blank = True, null=True)