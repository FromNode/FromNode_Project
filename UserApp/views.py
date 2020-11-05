from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Profile
from .forms import UserForm, ProfileForm, LoginForm

# Create your views here.

def signup(request):
    
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password('request["password"]')
            user.save()
            user.profile.bio = profile_form.cleaned_data.get('bio')
            user.profile.location = profile_form.cleaned_data.get('location')
            user.profile.save()
            print('생성굳')
        return render(request,'ProjectApp/project_list.html')

    elif request.method == 'GET':
        user_form = UserForm()
        profile_form = ProfileForm()
        return render(request,'UserApp/signup.html',{'user_form':user_form,'profile_form':profile_form})
    else:
        return render(request,'ProjectApp/project_list.html')



def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request,username=username,password=password)
        if user is not None:
            auth.login(request, user)
            print('로그인굳',username,password,user)
            return redirect('project:project_list')
        print(username,password,user)
        return redirect('project:project_list')
    else:
        login_form = LoginForm()
        return render(request,'UserApp/login.html',{'login_form':login_form})

def logout(request):
    auth.logout(request)
    return redirect('project:project_list')

def mypage(request):
    return render(request,'UserApp/mypage.html',{})
