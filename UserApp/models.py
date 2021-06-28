import string
from random import choice

from colorfield.fields import ColorField
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from ProjectApp.models import Projects

media_path = settings.MEDIA_ROOT

def user_path(instance,filename):
    arr = [choice(string.ascii_letters) for _ in range(8)]
    pid = ''.join(arr)
    extension = filename.split('.')[-1]
    return 'profiles/%s.%s' % (pid, extension)
    

class Profile(models.Model):
    objects = models.Manager()
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name='Profile')
    nickname = models.CharField(max_length=50, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to = user_path,blank=True,default='MainApp\image\default_profile.png')
    user_color = ColorField(default='#FF0000')


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

class Dashboard_User(models.Model):
    objects = models.Manager()
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nodes = models.IntegerField(default=0)
    contribution = models.FloatField(default=0)
    comments = models.IntegerField(default=0)
