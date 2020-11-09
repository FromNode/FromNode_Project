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
            The_file = x.ownerFCode
    print(The_file,'hi')
    return render(request, 'NodeApp/node_list.html',{'node_objs':node_objs,'The_file':The_file})


def node_detail(request,node_Code):
    node_obj = Nodes.objects.filter(Code = node_Code)
    The_file = node_obj.ownerFCode
    print(The_file,'hi')
    return render(request, 'NodeApp/node_details.html', {'node_obj':node_obj,'The_file':The_file})

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
        