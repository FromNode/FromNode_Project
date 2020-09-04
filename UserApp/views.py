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
            user.profile.bio = profile_form.cleaned_data.get('bio')
            user.profile.location = profile_form.cleaned_data.get('location')
            user.profile.save()
        return render(request,'MainApp/index.html')

    elif request.method == 'GET':
        user_form = UserForm()
        profile_form = ProfileForm()
        return render(request,'UserApp/signup.html',{'user_form':user_form,'profile_form':profile_form})
    else:
        return render(request,'MainApp/index.html')



def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')

    else:
        login_form = LoginForm()
        return render(request,'UserApp/login.html',{'login_form':login_form})

def logout(request):
    auth.logout(request)
    return redirect('index')
def mypage(request):
    return render(request,'UserApp/mypage.html',{})
