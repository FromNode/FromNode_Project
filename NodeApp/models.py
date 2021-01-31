from django.db import models
from django.contrib.auth.models import User
from random import choice
import string
from uuid import uuid4
from datetime import datetime

def get_file_path(instance, filename):
    ymd_path = datetime.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    return '/'.join(['upload_file/', ymd_path, uuid_name])

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
    fileObj = models.FileField(upload_to=get_file_path, null=True, blank=False) #이 노드에 저장되어 있는 파일
    filename = models.CharField(max_length=256, null=True)
    previousCode = models.ForeignKey('self',on_delete=models.SET_NULL, null=True, blank=True) #이전 노드
    ownerPCode = models.ForeignKey('ProjectApp.projects', on_delete=models.CASCADE,default='0', null=True)#이 노드가 속해 있는 프로젝트
    ownerFCode = models.ForeignKey('FileApp.Files', on_delete=models.CASCADE)#이 노드가 속해 있는 프로젝트
    whoIsOwner = models.ForeignKey(User,on_delete = models.SET_NULL, null=True, blank=True)#이 노드를 만든 회원
    comment = models.CharField(max_length=200, blank = True, null=True, default='설명을써주세요')
    nodeName = models.CharField(max_length=100, blank = True, null=True)
    description = models.TextField(max_length=20000, blank = True, null=True)
    class Meta:
        ordering = ['ownerPCode', 'createdDate']
    def __str__(self):
        return str(self.Code)
