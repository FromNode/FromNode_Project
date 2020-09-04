from django.shortcuts import render,redirect
from .models import User,Profile
from .forms import UserForm

# Create your views here.

def signup(request):
    if request.method == 'POST':
        user = User()
        #profile = Profile()

        user_form = UserForm()
        profile_form = ProfileForm()

        if user_form.is_vaild() and profile_form.is_vaild():
            user.username = request.POST['username']
            user.password = request.POST['password']
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.save()
        return render(request,'MainApp/index.html')

    elif request.mehod == 'GET':
        return render(request,'UserApp/signup.html',{'user_form':user_form,'profile_form':profile_form})
    else:
        return render(request,'MainApp/index.html')

def login(request):
    return render()

def mypage(request):
    return render(request,'UserApp/mypage.html',{})