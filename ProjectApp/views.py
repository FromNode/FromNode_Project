from django.shortcuts import render, redirect
from .models import Projects
from django.contrib.auth.models import User
from django.contrib import auth
from UserApp.models import Profile
import random
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from notifications.signals import notify

# User 모델 불러오기
# 불러온 User 모델의 Projects 불러오기
# 불러온 Projects를 슬라이싱, 이후 이걸 포함하는지 아닌지 대조!

def show_project_list(request):
    proj_obj = []
    User_Profile = []
    User_Projects = []
    empty = ''
    if request.user.is_authenticated:
        User_Profile = Profile.objects.get(user=request.user)
        # filter는 쿼리셋 메소드를 가져오니까 get으로 값을 불러오세요!!!!!!
        User_Projects = User_Profile.projects.split(',')
    else:
        pass


    for i in User_Projects:
        proj_obj += Projects.objects.filter(name=i)
    if len(proj_obj) == 0:
        empty = '참여중인 프로젝트가 없습니다'
    return render(request, 'ProjectApp/project_list.html', {'proj_obj' : proj_obj,'empty':empty})

def show_project_detail(request):
    # project에 소속된 file들이 보여지는 detail화면으로 슝 !
    return render(request, 'FileApp/file_list.html')

def project_checkcode(request):
    Project = Projects.objects.all()
    Project_Codes = []
    for i in Project:
        Project_Codes.append(i.Code)
    if request.POST['Code'] in Project_Codes:
        Join_Project = Projects.objects.get(Code=request.POST['Code'])
        #이후는 알림 기능 배우고! Owner_User = User.objects.get(Username=Join_Project.whoIsOwner)
        message = Join_Project.name,"프로젝트에 대한 참가 요청이 전송되었습니다!"
    else:
        message = "해당 코드를 지닌 프로젝트가 존재하지 않습니다"

    proj_obj = []
    User_Profile = Profile.objects.get(user=request.user)
    # filter는 쿼리셋 메소드를 가져오니까 get으로 값을 불러오세요!!!!!!
    User_Projects = User_Profile.projects.split(',')

    for i in User_Projects:
        proj_obj += Projects.objects.filter(name=i)

    return render(request, 'ProjectApp/project_list.html', {'proj_obj' : proj_obj,'message': message})
# def form_create_project(request):
#     return render(request,'ProjectApp/form_create_project.html')


# def create_project(request):
#     proj_obj = Projects()
#     proj_obj.Code = random.randint(0,0xffffff)
#     proj_obj.name = request.GET['projectName']
#     proj_obj.whoIsOwner = User.objects.get(username = 'sea')
#     proj_obj.save()
#     return redirect('project_list')

def create_project(request):
    proj_obj = Projects()
    proj_obj.Code = random.randint(0,0xffffff)
    proj_obj.name = request.GET['projectName']
    proj_obj.whoIsOwner = User.objects.get(username = 'sea')
    proj_obj.save()
    return redirect('project_list')

# def logout(request):
#     auth.logout(request)s
#     return redirect('/')
