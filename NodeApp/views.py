from django.shortcuts import render, redirect
from .models import Nodes, TestNode
from django.contrib.auth.models import User

def version_all(request):
    # node_obj = Nodes.objects.all()
    node_obj = TestNode.objects.all()
    # Nodes.fileObj = request.FILES['fileObj']
    return render(request, 'NodeApp/version_all.html', {'node_obj':node_obj})


def node_detail(request):
    # node_obj = Nodes.objects.all()
    node_obj = TestNode.objects.all()
    return render(request, 'NodeApp/node_detail.html', {'node_obj':node_obj})

def Upload(request):
    nodes = TestNode()
    if (request.method == 'POST'):
        for files in request.FILES.getlist('myFile'):
            nodes.file = files
            nodes.save()
    else :
        pass
    return render(request, 'NodeApp/version_all.html')
        