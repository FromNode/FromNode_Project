from django.shortcuts import render

def show_project_detail(request):
    return render(request, 'NodeApp/project_detail.html')

def show_upload(request):
    return render(request, 'NodeApp/upload.html')