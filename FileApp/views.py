import os
import random
from collections import Counter

from django.contrib.auth.models import User
from django.core import serializers
from django.shortcuts import redirect, render, reverse
from NodeApp.models import Node_Comment, Nodes
from ProjectApp.models import Projects
from UserApp.models import Profile

from .analyze import (communication_frequency, contribution,
                      node_upload_distribution)
from .models import Files, board


def show_file_list(request,proj_Code):
    
    if request.user.is_authenticated:

        Users = request.user
        unliked_proj = Users.Joined_Unliked_Projects.all()
        liked_proj = Users.Joined_Liked_Projects.all()
        all_proj = unliked_proj.union(liked_proj)
        proj_obj = all_proj

        project = Projects.objects.get(Code=proj_Code)
        
        pro_name = project.name
        pro_code = proj_Code
        # 로그인 한 유저가 포함된 Project 정보 불러오는 부분
        proj_user = project.unliked_members.all().union(project.liked_members.all())
        # 프로젝트 유저 불러오는 부분
        node_objs = project.Proj_Nodes.all()
        # 프로젝트 속한 노드 정보 불러오는 부분


        total_comment = 0
        #total_comment위한 초기값 선언
        for i in proj_user:
            total_comment += i.dashboard_user_set.get(project=project.pk).comments
            

        if bool(node_objs) == True:            
            contribution_each = contribution(proj_user,len(node_objs),total_comment,project.pk)
            comment_each = communication_frequency(proj_user,total_comment,project.pk)
            node_upload_nums = node_upload_distribution(proj_user,node_objs)
            print(len(node_objs))
        else:
            contribution_each = 0
            comment_each = 0
            node_upload_nums = 0
            
    else:
        
        pass

    is_there_notice = False
    noticeboard = board.objects.filter(proj_id = project.pk)
    if noticeboard.count() != 0:
        is_there_notice = True
    project = Projects.objects.get(Code = proj_Code)
    pro_name = project.name

    empty = ''
    contents = {
        'proj_obj' : proj_obj,
        'pro_code': proj_Code,
        'pro_name':pro_name,
        'project':project.id, 
        'proj_user':proj_user,
        'proj_id':project.pk,
        'empty':empty,
        'is_there_notice':is_there_notice,
        'noticeboard':noticeboard,

        'graph_datas_1':comment_each,  
        'graph_datas_2':contribution_each,
        'graph_datas_3':node_upload_nums[0],
        'total_node':len(node_objs),
        'date_last_node':node_upload_nums[1],
        'total_comment':total_comment,
        }
    return render(request, 'FileApp/file_list.html', contents)


def add_notice(request):
    notice_text = request.POST['notice_text']
    proj_code = request.POST['proj_id']
    proj_obj = Projects.objects.get(Code = proj_code)
    user_id = request.user
    new_notice = board()
    new_notice.proj_id = proj_obj
    new_notice.user_id = user_id
    new_notice.notice = notice_text
    new_notice.save()

    next_url = '/file/file_list/'+str(proj_code)
    return redirect(next_url)
