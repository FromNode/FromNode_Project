from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Profile
from .forms import UserForm, ProfileForm

# Create your views here.

def signup(request):
    
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        return render(request,'MainApp/index.html')

    elif request.method == 'GET':
        user_form = UserForm()
        profile_form = ProfileForm()
        return render(request,'UserApp/signup.html',{'user_form':user_form,'profile_form':profile_form})
    else:
        return render(request,'MainApp/index.html')

def login(request):
    return render()

def mypage(request):
    return render(request,'UserApp/mypage.html',{})