from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Profile
from .forms import UserForm, ProfileForm, LoginForm
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
                user.profile.bio = profile_form.cleaned_data.get('bio')
                user.profile.location = profile_form.cleaned_data.get('location')
                user.profile.save()
                auth.login(request, user)
            else:
                return render(request,'UserApp/signup.html')
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
        print(user)
        if user is not None:
            auth.login(request, user)
            return redirect('project:project_list')
        else:
            return redirect('user:login')
    else:
        login_form = LoginForm()
        return render(request,'UserApp/login.html',{'login_form':login_form})

def logout(request):
    auth.logout(request)
    return redirect('project:project_list')

def mypage(request):
    return render(request,'UserApp/mypage.html',{})
