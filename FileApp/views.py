import os
import random
from collections import Counter

from django.contrib.auth.models import User
from django.core import serializers
from django.shortcuts import redirect, render, reverse
from NodeApp.models import Node_Comment, Nodes
from ProjectApp.models import Projects
from UserApp.models import Profile

from .models import Files, board

# def show_project_list(request):
#     proj_obj = []
#     User_Profile = Profile.objects.get(user=request.user)
#     # filter는 쿼리셋 메소드를 가져오니까 get으로 값을 불러오세요!!!!!!
#     User_Projects = User_Profile.projects.split(',')

#     for i in User_Projects:
#         proj_obj += Projects.objects.filter(name=i)
#     return render(request, 'ProjectApp/project_list.html', {'proj_obj' : proj_obj})

def anlayze(node_objs,project):
    node_nums = [0 ,0 ,0 ,0 ,0 ,0]
    last_node_time = ''
    file_infoes = []
    total_comments = ''
    proj_members = project.unliked_members.all().union(project.liked_members.all())
    contribution_list = []
    cl_ele = {}
    for member in proj_members:
        cl_ele[member.username] = 1
    for i in range(0,5):
        contribution_list.append(Counter(cl_ele))
    comment_num_ver_user = {}
    for member in proj_members:
        comment_num_ver_user[member.username] = 0
    nodes = node_objs
    timeline = []
    contribution = []
    for i in nodes:
        owner = i.whoIsOwner.username
        letters = i.added_letters
        date = i.createdDate
        contribution.append([owner,letters,date])

        comments = Node_Comment.objects.filter(node_code = i.Code)
        for j in comments:
            # 모든 node의 유저별 댓글 수 불러오기
            user =j.author_comment.username
            value = comment_num_ver_user.get(user)
            value +=1
            comment_num_ver_user[user] = value
                
                
            #멘션 불러오기
            mention = j.who_is_mentioned
            if mention != 'none':
                pass
        # 노드의 datetimeline을 불러오기
        timeline.append(i.createdDate)

    timeline.sort()
    # print(timeline)
    if timeline != []:

        # 맨 처음, 마지막 노드의 간격을 불러와 노드 전체로 나눈거랑 비교
        first_time = min(timeline)
        last_time = max(timeline)
        last_node_time = last_time
        if(first_time != last_time):
            total_time_gap = last_time-first_time
            phase_time_gap = total_time_gap/5

            p1 = first_time + phase_time_gap*1
            p2 = first_time + phase_time_gap*2
            p3 = first_time + phase_time_gap*3
            p4 = first_time + phase_time_gap*4

            c1 = {}
            c2 = {}
            c3 = {}
            c4 = {}
            c5 = {}
            for member in proj_members:
                c1[member.username] = 1
                c2[member.username] = 1
                c3[member.username] = 1
                c4[member.username] = 1
                c5[member.username] = 1


            for i in contribution:
                if i[2]<p1:
                    if i[1] == None:
                        c1[i[0]] = c1[i[0]]+ 0
                    else:
                        c1[i[0]] = c1[i[0]]+ i[1]
                elif i[2]>p1 and i[2]>=p2:
                    if i[1] == None:
                        c2[i[0]] = c2[i[0]]+ 0
                    else:
                        c2[i[0]] = c2[i[0]]+ i[1]
                elif i[2]>p2 and i[2]>=p3:
                    if i[1] == None:
                        c3[i[0]] = c3[i[0]]+ 0
                    else:
                        c3[i[0]] = c3[i[0]]+ i[1]
                elif i[2]>p3 and i[2]>=p4:
                    if i[1] == None:
                        c4[i[0]] = c4[i[0]]+ 0
                    else:
                        c4[i[0]] = c4[i[0]]+ i[1]
                else:
                    if i[1] == None:
                        c5[i[0]] = c5[i[0]]+ 0
                    else:
                        c5[i[0]] = c5[i[0]]+ i[1]

            contribution_ver_user = {}
            for member in proj_members:
                contribution_ver_user[member.username] = 0
            
            phase_node_num = []
            p1_list = []
            p2_list = []
            p3_list = []
            p4_list = []
            p5_list = []
                
            for n, i in enumerate(timeline):
                 if i<=p1:
                    p1_list.append(i)
                 elif i>p1 and i<=p2:
                    p2_list.append(i)
                 elif i>p2 and i<=p3:
                    p3_list.append(i)
                 elif i>p3 and i<=p4:
                    p4_list.append(i)
                 else:
                    p5_list.append(i)


            node_time_gap = []
                
            node_nums[1] += len(p1_list)
            node_nums[2] += len(p2_list)
            node_nums[3] += len(p3_list)
            node_nums[4] += len(p4_list)
            node_nums[5] += len(p5_list)

            # for n, i in enumerate(timeline):
            #     if n +1 != len(timeline) :
            #         time_gap = timeline[n+1] - timedelta(days=0)
            #         print(type(time_gap))
            #         day = int(time_gap.days)
            #         seconds = int(time_gap.seconds)
            #         time_gap = day*24*60*60 + seconds

            #         node_time_gap.append(time_gap)
                    
                
            contribution_list_file = []
                
            for i in range(0,5):
                if i == 0:
                    contribution_list_file.append(Counter(c1))
                elif i ==1:
                    contribution_list_file.append(Counter(c2))            
                elif i ==2:
                    contribution_list_file.append(Counter(c3))            
                elif i ==3:
                    contribution_list_file.append(Counter(c4))        
                elif i ==4:
                    contribution_list_file.append(Counter(c5))    
                
        else:
            contribution_list_file = []
            c1 = {}
            c2 = {}
            c3 = {}
            c4 = {}
            c5 = {}
            for member in proj_members:
                c1[member.username] = 1
                c2[member.username] = 1
                c3[member.username] = 1
                c4[member.username] = 1
                c5[member.username] = 1
            for i in range(0,5):
                if i == 0:
                    contribution_list_file.append(Counter(c1))
                elif i ==1:
                    contribution_list_file.append(Counter(c2))
                elif i ==2:
                    contribution_list_file.append(Counter(c3))
                elif i ==3:
                    contribution_list_file.append(Counter(c4))
                elif i ==4:
                    contribution_list_file.append(Counter(c5))

        
    for i in range(0,5):
        x = contribution_list[i] + contribution_list_file[i]
        # print(contribution_list[i],contribution_list_file[i])
        contribution_list[i]= (x)
        
    # 댓글 수 나눠서 기여도 체크
    all_comments_num = sum(i for i in comment_num_ver_user.values())
    # average_comments = all_comments_num / proj_members_num
    comment_info_ver_file = {}

    for i in comment_num_ver_user:
        comment_num = comment_num_ver_user[i]
        if all_comments_num == 0:
            contribute_ver_comments =0 
        else:
            contribute_ver_comments = round(comment_num / all_comments_num *100 ,2)
        # 파일별 유저 기여도_코멘트 수
        comment_info_ver_file[i] = comment_num
        
    file_infoes.append(comment_info_ver_file)
    
    
    new_list = []
    for n, i in enumerate(file_infoes):
        count = Counter(i)
        new_list.append(count)

    y = new_list[0]
    for i in range(1,len(new_list)):
        x = new_list[i]
        y += x
    user_proj_comments = dict(y)
    for user in user_proj_comments:
        comment_num_ver_user[user] = user_proj_comments[user]

    news = []
    for i in contribution_list:
        new = dict(i)
        print(new)
        news.append(new)

    
    total_proj_comments = sum(dict(y).values())

    total_node = sum(node_nums)

    return comment_num_ver_user,news,node_nums,total_node, last_node_time, total_proj_comments

def show_file_list(request,proj_Code):
    
    if request.user.is_authenticated:
        User = request.user
        unliked_proj = User.Joined_Unliked_Projects.all()
        liked_proj = User.Joined_Liked_Projects.all()
        all_proj = unliked_proj | liked_proj
        proj_obj = all_proj
        project = Projects.objects.get(Code = proj_Code)
        proj_id = project.id
        proj_user = project.unliked_members.all().union(project.liked_members.all())
        node_objs = project.Proj_Nodes.all()
        if bool(node_objs) == True:            
            graph_datas = anlayze(node_objs, project)
        else:
            graph_datas = [1,2,3,0,0,0]
    else:
        
        pass
    is_there_notice = False
    noticeboard = board.objects.filter(proj_id = proj_id)
    if noticeboard.count() != 0:
        is_there_notice = True
    project = Projects.objects.get(Code = proj_Code)
    pro_name = project.name
    # detail pro name 뽑아오는 과정
    # proj_user = []

    empty = ''
    contents = {
        'proj_obj' : proj_obj,
        'pro_code': proj_Code,
        'pro_name':pro_name,
        'project':project.id, 
        'proj_user':proj_user,
        'proj_id':proj_id,
        'empty':empty,
        'is_there_notice':is_there_notice,
        'noticeboard':noticeboard,
        'graph_datas_1':graph_datas[0],  
        'graph_datas_2':graph_datas[1],
        'graph_datas_3':graph_datas[2],
        'total_node':graph_datas[3],
        'date_last_node':graph_datas[4],
        'total_comment':graph_datas[5],
        }
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

# def create_new_file(request):
#     pk = request.POST['pk']
#     user_write_f_name = request.POST['file_name']
#     next_url = '/file/file_list/'+str(pk)
#     filename = request.FILES['myFile']
#     fileExtension = str(filename).split('.')[1]
#     #str(filename).split('.')[0] 디폴트 파일 명
#     file_obj = Files()
#     file_obj.fileName = request.POST['file_name']
#     file_obj.whoIsOwner = request.user
#     file_obj.ownerPCode = Projects.objects.get(id=request.POST['pk'])
#     file_obj.description = "파일 설명 필드 지금 안쓴다."
#     if(fileExtension == 'pptx'):
#         file_obj.image = 'ppt'
#     elif(fileExtension =='doc' or fileExtension == 'docx'):
#         file_obj.image = 'word'
#     elif(fileExtension=='pdf'):
#         file_obj.image = 'pdf'
#     else:
#         file_obj.image = 'etc'
#     file_obj.save()
#     # first node
#     node_obj = Nodes()
#     node_obj.fileObj = request.FILES['myFile']
#     node_obj.ownerPCode = Projects.objects.get(id=request.POST['pk'])
#     node_obj.ownerFCode = file_obj
#     node_obj.comment = request.POST['file_name']
#     node_obj.filename = request.FILES['myFile'].name
#     node_obj.whoIsOwner = request.user
#     node_obj.save()
#     file_obj.File_Nodes.add(node_obj)
#     file_obj.save()

#     return redirect(next_url)
    

# def create_invite_url(request, project_id):
#     if request.user.is_authenticated:
#         project_code = Projects.objects.get(id = project_id).Code
#         invite_url = project_code
#         return render(request, 'FileApp/create_invite_url.html', {'invite_url':invite_url})
#     else:
#         return render(request, 'error')
