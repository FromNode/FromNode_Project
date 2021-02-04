from django.db import models

from django.contrib.auth.models import User #일단 user의 아이디값으로 받아오는걸로 !

class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now = True)

    # 아래의 두줄이 TImeStampedModel을 abstrat base class로 만들어준다.
    # 마이그레이션 할때 테이블이 생성되지 않게된다.
    # 아래 두줄을 넣게 되면, 이 class를 상속받는 모든 클래스들이 자신만의 타임스탬프 필드를 가지게 된다.
    class Meta:
        abstract = True

class Notification(TimeStampedModel): # 위에 작성한 TimeStampedModel 상속받은거다. TimeSpampedModel의 특징은 여기저기 사용되기에 core가 있으면 좋을 듯.
    # 필요한건 .. 내게 변화를 준
    # 유저이름, 유저가 속한 프로젝트, 몇 일이 지났는가, 작성된댓글내용, 타입(댓글, 새로운팀원, 멘션)
    TYPE_CHOICES = (
        ('comment', 'Comment'),
        ('new_member', 'New_member'),
        ('mention', 'Mention')
    )
    
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='creator')
    to = models.ForeignKey(User, on_delete=models.PROTECT, related_name='to')
    Notification_type = models.CharField(max_length = 20, choices=TYPE_CHOICES)