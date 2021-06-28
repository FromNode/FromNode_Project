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

        # 로그인 한 유저가 포함된 Project를 역참조로 불러옵니다.
        project = Projects.objects.get(Code=proj_Code)
        node_objs = project.Proj_Nodes.all()
        pro_name = project.name
        pro_code = proj_Code
        proj_user = project.unliked_members.all().union(project.liked_members.all())
        total_comment = 0

        for i in proj_user:
            total_comment += i.comments

        if bool(node_objs) == True:            
            contribution_each = contribution(proj_user,node_objs,total_comment)
            comment_each = communication_frequency(proj_user,total_comment)
            node_upload_nums = node_upload_distribution(proj_user)

        else:
            graph_datas = [1,2,3,0,0,0]
    else:
        
        pass

    is_there_notice = False
    noticeboard = board.objects.filter(proj_id = pro_code)
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
        'proj_id':pro_code,
        'empty':empty,
        'is_there_notice':is_there_notice,
        'noticeboard':noticeboard,

        'graph_datas_1':comment_each,  
        'graph_datas_2':contribution_each,
        'graph_datas_3':node_upload_nums,
        'total_node':len(node_objs),
        'date_last_node':node_objs[-1].createDate,
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
