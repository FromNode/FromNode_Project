from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

# 자동로그인
def index(request):
    return render(request, 'MainApp/index.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('index')
    return render(request, 'MainApp/index.html')
    