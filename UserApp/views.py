from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Profile
from ProjectApp.models import Projects
from .forms import UserForm, ProfileForm, LoginForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from notifications.signals import notify
# Create your views here.

def signup(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['confirm']:
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
            # user_form = UserForm(request.POST)
            profile_form = ProfileForm(request.POST)
            # user_form_password = request.POST['password']
            # user = user_form.save()
            # user.set_password(user_form_password)
            # user.save()
            if profile_form.is_valid():
                #이 밑에 저거 왜 필요한지 모르겠어서 일단 주석해둘게요 ,, 
                '''
                user.profile.bio = profile_form.cleaned_data.get('bio')
                user.profile.location = profile_form.cleaned_data.get('location')
                user.profile.save()
                '''
                auth.login(request, user)
                redirect('project:project_list')
            else:
                return redirect('user:login')
        return render(request,'ProjectApp/project_list.html')

    elif request.method == 'GET':
        user_form = UserForm()
        profile_form = ProfileForm()
        return render(request,'UserApp/signup.html',{'user_form':user_form,'profile_form':profile_form})
    else:
        return render(request,'ProjectApp/project_list.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None: #스무스하게 로그인
            auth.login(request, user)
            return redirect('project:project_list')
        else: #뭔가 잘못쳤을 때
            hidden = 0
            message = '로그인 정보가 옳지 않아요!'
            return render(request,'MainApp/index.html',{'hidden':hidden,'message':message})
    else:
        login_form = LoginForm()
        return render(request,'UserApp/login.html',{'login_form':login_form})

def logout(request):
    auth.logout(request)
    return redirect('index')

def mypage(request):
    recipients = User.objects.all()
    user = request.user
    if user in recipients:
        unread_messages = user.notifications.unread()
        unread_messages_invite = unread_messages.filter(description = 1)
        # for i in unread_messages_invite:
        #     invite_code = i.verb
        #     project_name = Projects.objects.get(Code = invite_code)
            # i.append({'project_name':project_name})
            # print(i)
        print(unread_messages_invite)
        unread_messages_invite_return = unread_messages.filter(description = 2)
        return render(request,'UserApp/mypage.html',{'unread_messages':unread_messages,'unread_messages_invite':unread_messages_invite,'unread_messages_invite_return':unread_messages_invite_return})
    return render(request,'UserApp/mypage.html',{})

def join_project(request):
    recipient = request.user
    actor = User.objects.get(username=request.POST['actor'])
    project = request.POST['project']
    proj_request = recipient.notifications.filter(verb=project)
    if request.method == 'POST':
        for i in proj_request:
            if actor == i.actor:
                print(project)
                notify.send(request.user,recipient = i.actor,verb = request.user.username+'님이'+project+"참가를 허용하셨습니다!", description = 2 )
                i.mark_as_read()
                join_project = Projects.objects.get(Code = project)
                join_project.members.add(i.actor)
                join_project.save()
        # User_Profile = Profile.objects.get(user=actor)
        # User_Profile.projects += ','+project
        # User_Profile.save()
        return redirect('user:mypage')
    else:
        for i in proj_request:
            if actor == i.actor:
                i.mark_as_read()
        return redirect('user:mypage')
    

def cofirm_alarm(request):
    recipient = request.user
    actor = User.objects.get(username=request.POST['actor'])
    project = request.POST['project']
    proj_request = recipient.notifications.filter(verb=project)
    if request.method == 'POST':
        for i in proj_request:
            if actor == i.actor:
                i.mark_as_read()
        return redirect('user:mypage')
        
    return redirect('user:mypage')

