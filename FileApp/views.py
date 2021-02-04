from django.shortcuts import render, redirect, reverse
from .models import Files, board
from NodeApp.models import Nodes
from ProjectApp.models import Projects
from django.contrib.auth.models import User
from UserApp.models import Profile
import os
import random

# def show_project_list(request):
#     proj_obj = []
#     User_Profile = Profile.objects.get(user=request.user)
#     # filter는 쿼리셋 메소드를 가져오니까 get으로 값을 불러오세요!!!!!!
#     User_Projects = User_Profile.projects.split(',')

#     for i in User_Projects:
#         proj_obj += Projects.objects.filter(name=i)
#     return render(request, 'ProjectApp/project_list.html', {'proj_obj' : proj_obj})

def show_file_list(request,project_id):
    if request.user.is_authenticated:
        User = request.user
        unliked_proj = User.Joined_Unliked_Projects.all()
        liked_proj = User.Joined_Liked_Projects.all()
        all_proj = unliked_proj | liked_proj
        proj_obj = all_proj
    else:
        pass
    
    is_there_notice = False
    noticeboard = board.objects.filter(proj_id = project_id)
    if noticeboard.count() != 0:
        is_there_notice = True


    project = Projects.objects.get(id = project_id)
    pro_name = project.name
    # detail pro name 뽑아오는 과정
    proj_user = []

    empty = ''
    file_obj = Files.objects.filter(ownerPCode=project_id)
    
    if len(file_obj) == 0:
        empty = '추적한 파일이 없습니다'
    
    contents = {
        'proj_obj':proj_obj,
        'pro_name':pro_name,
        'project':project.id, 
        'file_obj':file_obj,
        'proj_user':proj_user,
        'empty':empty,
        'project_id':project_id,
        'is_there_notice':is_there_notice,
        'noticeboard':noticeboard,
        }
    print(is_there_notice)
    return render(request, 'FileApp/file_list.html', contents)

def add_notice(request):
    notice_text = request.POST['notice_text']
    proj_id = request.POST['proj_id']
    proj_obj = Projects.objects.get(id = proj_id)
    user_id = request.user
    new_notice = board()
    new_notice.proj_id = proj_obj
    new_notice.user_id = user_id
    new_notice.notice = notice_text
    new_notice.save()

    next_url = '/file/file_list/'+str(proj_id)
    return redirect(next_url)
# def form_create_new_file(request):
#     return render(request, 'FileApp/form_create_new_file.html')

# def show_upload(request):
#     return render(request, 'FileApp/upload.html')

def create_new_file(request):
    pk = request.POST['pk']
    next_url = '/file/file_list/'+str(pk)
    filename = request.FILES['myFile']
    fileExtension = str(filename).split('.')[1]
    #str(filename).split('.')[0] 디폴트 파일 명
    file_obj = Files()
    file_obj.fileName = request.POST['fileName']
    file_obj.whoIsOwner = request.user
    file_obj.ownerPCode = Projects.objects.get(id=request.POST['pk'])
    file_obj.description = request.POST['fileMemo']
    if(fileExtension == 'pptx'):
        file_obj.image = 'ppt'
    elif(fileExtension =='doc' or fileExtension == 'docx'):
        file_obj.image = 'word'
    elif(fileExtension=='pdf'):
        file_obj.image = 'pdf'
    else:
        file_obj.image = 'etc'
    file_obj.save()
    # first node
    node_obj = Nodes()
    node_obj.fileObj = request.FILES['myFile']
    node_obj.ownerPCode = Projects.objects.get(id=request.POST['pk'])
    node_obj.ownerFCode = file_obj
    node_obj.whoIsOwner = request.user
    node_obj.save()

    return redirect(next_url)
    

def create_invite_url(request, project_id):
    if request.user.is_authenticated:
        project_code = Projects.objects.get(id = project_id).Code
        invite_url = project_code
        return render(request, 'FileApp/create_invite_url.html', {'invite_url':invite_url})
    else:
        return render(request, 'error')