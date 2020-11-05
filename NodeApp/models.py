from django.db import models
from django.contrib.auth.models import User

class Nodes(models.Model):
    Code = models.CharField(primary_key = True, max_length=255, default=0, unique=True) #노드별 고유 코드
    createdDate = models.DateTimeField(auto_now=True)
    fileObj = models.FileField(upload_to="media", blank=False) #이 노드에 저장되어 있는 파일
    previousCode = models.ForeignKey('self',on_delete=models.SET_NULL, null=True, blank=True) #이전 노드
    ownerPCode = models.ForeignKey('ProjectApp.projects', on_delete=models.CASCADE)#이 노드가 속해 있는 프로젝트
    ownerFCode = models.ForeignKey('FileApp.Files', on_delete=models.CASCADE)#이 노드가 속해 있는 프로젝트
    whoIsOwner = models.ForeignKey(User,on_delete = models.SET_NULL, null=True, blank=True)#이 노드를 만든 회원
    
class TestNode(models.Model):
    file = models.FileField(upload_to="test")