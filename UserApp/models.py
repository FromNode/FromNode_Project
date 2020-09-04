from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    # 추가 할 오브젝트는 이 공간에 써주면 되어요
    
@receiver(post_save,sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    
@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    instance.Profile.save()
# receiver는 이벤트가 발생 할 때 찾는 놈입니다. 
# save가 발생 할 때 마다 create_user_profile/save_user_profile로 Profile도 같이 생성되게 하는 놈이에여
# 결론 = 지우지마!