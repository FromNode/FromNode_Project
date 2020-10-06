from django.shortcuts import render
from .models import Nodes

def show_project_detail(request):
    node_all = Nodes.objects.all
    return render(request, 'NodeApp/project_detail.html', {'node_all':node_all})

def show_upload(request):
    return render(request, 'NodeApp/upload.html')