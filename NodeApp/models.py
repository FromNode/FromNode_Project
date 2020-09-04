from django.db import models
from ProjectApp import models
from UserApp import models

class Nodes(models.Model):
    ID = models.CharField(primary_key = True, default=0, unique=True) #노드별 고유 코드
    createdDate = models.DateTimeField(auto_now=True)
    fileObj = models.FileField(upload_to="media", blank=False) #이 노드에 저장되어 있는 파일
    previousID = models.ForeignKey('self',on_delete=SET_NULL, null=True, blank=True) #이전 노드
    ownerProjectID = models.ForeignKey('ProjectApp.projects'on_delete=models.CASCADE)#이 노드가 속해 있는 프로젝트
    whoIsOwner = models.ForeignKey('',)#이 노드를 만든 회원
    ''' 
    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    '''