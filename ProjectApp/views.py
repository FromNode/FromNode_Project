from django.shortcuts import render, redirect
from .models import Projects, proj_with_user
from FileApp.models import Files
from NodeApp.models import Nodes, Node_Comment
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
from django.http import HttpResponse

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

def anlayze(files, project):
    file_infoes = {}
    
    proj_members = project.unliked_members.all().union(project.liked_members.all())
    for x in files:
        comment_num_ver_user = {}
        for member in proj_members:
            comment_num_ver_user[member.username] = 0
        nodes = Nodes.objects.filter(ownerFCode = x)
        timeline = []
        for i in nodes:
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
            if(first_time != last_time):
                total_time_gap = last_time-first_time
                day = int(total_time_gap.days)
                seconds = int(total_time_gap.seconds)
                # 평균 gap 계산
                sorted_by_seconds = day*24*60*60 + seconds
                averge_time_gap = round(sorted_by_seconds/len(nodes),3)
                print(averge_time_gap)

                node_time_gap = []

                for n, i in enumerate(timeline):
                    if n +1 != len(timeline) :
                        time_gap = timeline[n+1] - timeline[n]
                        day = int(time_gap.days)
                        seconds = int(time_gap.seconds)
                        time_gap = day*24*60*60 + seconds

                        node_time_gap.append(time_gap)
                

            else:
                print('첫 노드')

                
    
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
            comment_info_ver_file[i] = [comment_num,contribute_ver_comments]
        
        file_infoes[x] = comment_info_ver_file

    print(file_infoes)
    total_comments = []

    print(total_comments)
            
        

        # 파일 업로드 오너 유저 불러오기
        # 업로드 점유율 체크


def proj_contributions(request,project_Code):
    if request.user.is_authenticated:
        t_comment_num_ver_user = []
        t_node_timeline_gap = []
        t_file_upload_ver_user = []

        The_Project = Projects.objects.get(Code = project_Code)
        files = Files.objects.filter(ownerPCode = The_Project)
        anlayze(files, The_Project)
        
        objects ={

        }

        return render(request, 'ProjectApp/proj_contributions.html', objects)

    else:
        return render(request,'MainApp/index.html')

    

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
    return render(request, 'ProjectApp/error.html')


def already_exist(request):
    return render(request, 'ProjectApp/already.html')


def confirm_project_checkin(request, project_Code):
    target_project = Projects.objects.get(Code = project_Code)
    return render(request, 'ProjectApp/confirm_project_checkin.html', {'target_project':target_project})


def project_checkin(request):
    if request.method == 'POST':
        project_code = request.POST['project_code']
        if request.user.is_authenticated:
            user = request.user
            project_obj = Projects.objects.get(Code=project_code)
            project_member = proj_with_user.objects.filter(proj_id = project_obj.id)
            for member in project_member:
                if member.user_id == user.id: #내가 안속해있는 프로젝트인지 확인
                    return redirect('project:already_exist')
                else:
                    project_obj.unliked_members.add(user)
                    project_obj.save()
                    try:
                        p_w_u_obj =proj_with_user();
                        p_w_u_obj.proj_id = project_obj
                        p_w_u_obj.user_id = user
                        p_w_u_obj.save()
                        return redirect('project:project_list')
                    except:
                        project_obj.unliked_members.remove(user)
                        project_obj.save()
                        return redirect('project:error')
        else:
            request.COOKIES['project_code']=project_code
            response = render(request, 'UserApp/login.html')
            response.set_cookie(key='project_code', value=project_code)
            return response
    else:
        return redirect('main:index')
    
