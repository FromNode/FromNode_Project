from django.shortcuts import render, redirect
from .models import Projects, proj_with_user
from django.contrib.auth.models import User
from django.contrib import auth
from UserApp.models import Profile
import random
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from notifications.signals import notify
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Q

# User 모델 불러오기
# 불러온 User 모델의 Projects 불러오기
# 불러온 Projects를 슬라이싱, 이후 이걸 포함하는지 아닌지 대조!

def show_project_list(request):
    #Page 파라미터
    page = request.GET.get('page', '1')
    # 모든 프로젝트의 모든 member를 순차 조회
    if request.user.is_authenticated:
        User = request.user
        unliked_proj = User.Joined_Unliked_Projects.all()
        liked_proj = User.Joined_Liked_Projects.all()
        all_proj = unliked_proj | liked_proj
        # paginator = Paginator(all_proj, 4)  # 페이지당 10개씩 보여주기
        # page_obj = paginator.get_page(page)
        proj_obj = all_proj
    empty = ''
    if len(proj_obj) == 0:
        empty = '참여중인 프로젝트가 없습니다'
    today = datetime.today()
    contents = {
        'proj_obj' : proj_obj,
        'empty':empty, 
        'today':today,
        'proj_obj_all':all_proj,
        'like_proj':liked_proj
    }
    return render(request, 'ProjectApp/project_list.html', contents)

def show_project_detail(request):
    # project에 소속된 file들이 보여지는 detail화면으로 슝 !
    return render(request, 'FileApp/file_list.html')

def project_checkcode(request):
    Project = Projects.objects.all()
    if request.user.is_authenticated:
        proj_obj = Projects.objects.filter(members = request.user)
    Project_Codes = []
    for i in Project:
        Project_Codes.append(i.Code)
    if request.POST['Code'] in Project_Codes:
        Join_Project = Projects.objects.get(Code=request.POST['Code'])
        Owner = Join_Project.members.all()[0]
        recipients = User.objects.get(username = Owner)
        notify.send(request.user,recipient = recipients,verb = Join_Project.Code, description = 1)
        
        #이후는 알림 기능 배우고! Owner_User = User.objects.get(Username=Join_Project.whoIsOwner)
        # 코드를 보내면서, 동시에 해당 코드를 가진 프로젝트의 오너한테 알림을 보낼것!
        message = Join_Project.name,"프로젝트에 대한 참가 요청이 전송되었습니다!"
    else:
        message = "해당 코드를 지닌 프로젝트가 존재하지 않습니다"
        
    return render(request, 'ProjectApp/project_list.html', {'proj_obj' : proj_obj,'message': message})

def likeornot(request ,project_Code):
    code = project_Code
    User =request.user
    proj_obj = Projects.objects.get(Code=code)
    unliked_proj = User.Joined_Unliked_Projects.all()
    if  proj_obj in unliked_proj:
        proj_obj.unliked_members.remove(User)
        proj_obj.liked_members.add(User)
        proj_obj.save()
    else:
        proj_obj.liked_members.remove(User)
        proj_obj.unliked_members.add(User)
        proj_obj.save()
    return redirect('/project/project_list/')


    

# def form_create_project(request):
#     return render(request,'ProjectApp/form_create_project.html')

# def create_project(request):
#     proj_obj = Projects()
#     proj_obj.Code = random.randint(0,0xffffff)
#     proj_obj.name = request.GET['projectName']
#     proj_obj.whoIsOwner = User.objects.get(username = 'sea')
#     proj_obj.save()
#     return redirect('project_list')

# def create_project(request):
#     proj_obj = Projects()
#     proj_obj.Code = random.randint(0,0xffffff)
#     proj_obj.name = request.GET['projectName']
#     proj_obj.whoIsOwner = User.objects.get(username = 'sea')
#     proj_obj.save()
#     return redirect('project_list')

# def logout(request):
#     auth.logout(request)s
#     return redirect('/')

def project_create(request):
    if request.method == 'POST':
        user = request.user
        proj_obj = Projects()
        proj_obj.name = request.POST['name']
        proj_obj.save()
        proj_obj.unliked_members.add(user)
        proj_obj.save()
        User_Profile = Profile.objects.get(user=request.user)
        User_Profile.save()
        try:
            p_w_u_obj =proj_with_user();
            p_w_u_obj.proj_id = Projects.objects.get(name=proj_obj.name)
            p_w_u_obj.user_id = user
            p_w_u_obj.save()
            return redirect('project:project_list')
        except:
            Projects.objects.last.delete()
            return redirect('project:error')
    else:
        return redirect('project:project_list')


def error(request):
    return render('project:error')