from django.shortcuts import render

def show_project_list(request):
    return render(request, 'ProjectApp/project_list.html')
def create_project(request):
    return render(request, 'ProjectApp/create_proj.html')