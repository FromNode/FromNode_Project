from django.shortcuts import render, redirect
from .models import Files
from ProjectApp.models import Projects
from django.contrib.auth.models import User
import random

def show_file_list(request):
    file_obj = Files.objects.all()
    return render(request, 'FileApp/file_list.html', {'file_obj':file_obj})

# def form_create_new_file(request):
#     return render(request, 'FileApp/form_create_new_file.html')

# def show_upload(request):
#     return render(request, 'FileApp/upload.html')

# def create_new_file(request):
#     file_obj = Files()
#     file_obj.fileName = "따뜻한라떼"
#     file_obj.Code = random.randint(0,0xffffff)
#     file_obj.whoIsOwner = User.objects.get(username = 'sea')
#     file_obj.ownerPCode = Projects.objects.get(name = 'proscons')
#     file_obj.save()
#     return redirect('project_detail')
    
