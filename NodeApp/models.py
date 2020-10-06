from django.db import models
from django.contrib.auth.models import User

class Nodes(models.Model):
    Code = models.CharField(primary_key = True, max_length=255, default=0, unique=True) #노드별 고유 코드
    createdDate = models.DateTimeField(auto_now=True)
    fileObj = models.FileField(upload_to="media", blank=False) #이 노드에 저장되어 있는 파일
<<<<<<< HEAD
    previousCode = models.ForeignKey('self',on_delete=models.SET_NULL, null=True, blank=True) #이전 노드
    ownerPCode = models.ForeignKey('ProjectApp.projects', on_delete=models.CASCADE)#이 노드가 속해 있는 프로젝트
    whoIsOwner = models.ForeignKey(User,on_delete = models.SET_NULL, null=True, blank=True)#이 노드를 만든 회원
=======
    previousID = models.ForeignKey('self',on_delete=models.SET_NULL, null=True, blank=True) #이전 노드
    ownerProjectID = models.ForeignKey('ProjectApp.Projects', on_delete=models.CASCADE)#이 노드가 속해 있는 프로젝트
    whoIsOwner = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)#이 노드를 만든 회원
>>>>>>> 93ec2910d097ff6e53e6d82d94a529fc169e862f
    
    
    #def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    #    return ''.join(random.choice(chars) for _ in range(size))
    #