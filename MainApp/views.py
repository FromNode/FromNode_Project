from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def index(request):
    if User.is_authenticated:
        return redirect('project:project_list')

    return render(request, 'MainApp/index.html')