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

def create_node(request, node_Code):
    PNode = Nodes.objects.get(Code=node_Code)
    The_file = PNode.ownerFCode
    A = Nodes.objects.all()
    node_objs =Nodes.objects.filter(ownerFCode = The_file)

    if request.method == 'POST':
        node_obj = Nodes()
        node_obj.fileObj = request.FILES['File']
        node_obj.previousCode = PNode.Code
        node_obj.ownerFCode = PNode.ownerFCode
        node_obj.ownerPCode = PNode.ownerPCode
        node_obj.whoIsOwner = reuqest.user
        node_obj.save()

        return render(request,'NodeApp/node_list.html',{'node_objs':node_objs,'The_file':The_file})
    else:
        return render(request,'NodeApp/create_node.html',{})

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
        