from django.shortcuts import render, redirect
from .models import Nodes, TestNode
from ProjectApp.models import Projects
from django.contrib.auth.models import User
from datetime import datetime

def version_all(request):
    node_objs = Nodes.objects.all()
    return render(request, 'NodeApp/version_all.html', {'node_objs':node_objs})


def node_detail(request):
    # node_obj = Nodes.objects.all()
    node_obj = TestNode.objects.all()
    return render(request, 'NodeApp/node_detail.html', {'node_obj':node_obj})

def Upload(request):
    '''
    nodes = TestNode()
    if (request.method == 'POST'):
        for files in request.FILES.getlist('myFile'):
            nodes.file = files
            nodes.save()
    else :
        pass
    '''

    nodeobj = Nodes()
    nodeobj.Code = "001000"
    nodeobj.createdDate = datetime.now
    for files in request.FILES.getlist('myFile'):
         nodeobj.fileObj = files
    nodeobj.previousCode =Nodes.objects.get(Code="000001") 
    nodeobj.ownerPCode = Projects.objects.get(Code="000001")
    nodeobj.whoIsOwner = User.objects.get(username = 'sea')
    nodeobj.save()
    
    return render(request, 'NodeApp/version_all.html')
        