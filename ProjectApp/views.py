from django.shortcuts import render, redirect
from .models import Projects
from django.contrib.auth.models import User
import random

def show_project_list(request):
    proj_obj = Projects.objects.all()
    return render(request, 'ProjectApp/project_list.html', {'proj_obj' : proj_obj})


def form_create_project(request):
    return render(request,'ProjectApp/form_create_project.html')


def create_project(request):
    proj_obj = Projects()
    proj_obj.Code = random.randint(0,0xffffff)
    proj_obj.name = request.GET['projectName']
    proj_obj.whoIsOwner = User.objects.get(username = 'sea')
    proj_obj.save()
    return redirect('project_list')

# def logout(request):
#     auth.logout(request)
#     return redirect('/')