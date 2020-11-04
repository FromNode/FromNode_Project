from django.shortcuts import render, redirect
from .models import Projects
from django.contrib.auth.models import User
from UserApp.models import Profile
import random

# User 모델 불러오기
# 불러온 User 모델의 Projects 불러오기
# 불러온 Projects를 슬라이싱, 이후 이걸 포함하는지 아닌지 대조!

def show_project_list(request):
    proj_obj = []
    User_Profile = Profile.objects.get(user=request.user)
    # filter는 쿼리셋 메소드를 가져오니까 get으로 값을 불러오세요!!!!!!
    User_Projects = User_Profile.projects.split(',')

    for i in User_Projects:
        proj_obj += Projects.objects.filter(name=i)
    return render(request, 'ProjectApp/project_list.html', {'proj_obj' : proj_obj})


def form_create_project(request):
    return render(request,'ProjectApp/form_create_project.html')


def create_project(request):
    proj_obj = Projects()
    proj_obj.Code = random.randint(0,0xffffff)
    proj_obj.name = request.GET['projectName']
    proj_obj.whoIsOwner = User.objects.get(username = 'sea')
    proj_obj.save()
    return redirect('project_list')

