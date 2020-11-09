from django.shortcuts import render, redirect
from .models import Nodes, TestNode
from FileApp.models import Files
from ProjectApp.models import Projects
from django.contrib.auth.models import User
from datetime import datetime

def version_all(request,file_Code):
    The_File = Files.objects.get(Code=file_Code)
    A = Nodes.objects.all()
    node_objs =[]
    for x in A:
        if x.ownerFCode.Code == The_File.Code:
            node_objs.append(x)
    return render(request, 'NodeApp/node_list.html',{'node_objs':node_objs})


def node_detail(request,node_Code):
    node_obj = Nodes.objects.filter(Code = node_Code)
    return render(request, 'NodeApp/node_details.html', {'node_obj':node_obj})

def Upload(request):
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
        