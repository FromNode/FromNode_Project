from django.shortcuts import render, redirect
from .models import Files
from ProjectApp.models import Projects
from django.contrib.auth.models import User
from UserApp.models import Profile
import random

# def show_project_list(request):
#     proj_obj = []
#     User_Profile = Profile.objects.get(user=request.user)
#     # filter는 쿼리셋 메소드를 가져오니까 get으로 값을 불러오세요!!!!!!
#     User_Projects = User_Profile.projects.split(',')

#     for i in User_Projects:
#         proj_obj += Projects.objects.filter(name=i)
#     return render(request, 'ProjectApp/project_list.html', {'proj_obj' : proj_obj})

def show_project_detail(request,project_id):
    project = Projects.objects.get(id = project_id)
    pro_name = project.name
    # detail pro name 뽑아오는 과정
    proj_obj = []
    proj_user = []
    # for문 위한 초기 선언
    for x in Profile.objects.all():
        a = x.projects.split(',')
        proj_obj = a
        if pro_name in proj_obj:
            proj_user.append(x.user)
    # for문 지나서 project 가진 user 정보들이 list로 뽑힙니다
    file_obj = Files.objects.filter(ownerPCode=project_id)
    return render(request, 'FileApp/project_detail.html', {'file_obj':file_obj,'proj_user':proj_user,})
def show_file_list(request):
    file_obj = Files.objects.all()
    return render(request, 'FileApp/file_list.html', {'file_obj':file_obj})

# def form_create_new_file(request):
#     return render(request, 'FileApp/form_create_new_file.html')

# def show_upload(request):
#     return render(request, 'FileApp/upload.html')

# def create_new_file(request):
#     file_obj = Files()
#     file_obj.fileName = "따뜻한라떼"
#     file_obj.Code = random.randint(0,0xffffff)
#     file_obj.whoIsOwner = User.objects.get(username = 'sea')
#     file_obj.ownerPCode = Projects.objects.get(name = 'proscons')
#     file_obj.save()
#     return redirect('project_detail')
    
