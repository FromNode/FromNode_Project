from django.shortcuts import render, redirect
from .models import Nodes
from FileApp.models import Files
from ProjectApp.models import Projects
from django.contrib.auth.models import User
from datetime import datetime
from django.core import serializers
from UserApp.models import Profile

def node_list(request,file_Code):
    proj_obj = []
    User_Profile = []
    User_Projects = []
    if request.user.is_authenticated:
        User_Profile = Profile.objects.get(user=request.user)
        # filter는 쿼리셋 메소드를 가져오니까 get으로 값을 불러오세요!!!!!!
        User_Projects = User_Profile.projects.split(',')
    else:
        pass


    for i in User_Projects:
        proj_obj += Projects.objects.filter(name=i)

    

    The_file = Files.objects.get(Code=file_Code)
    project = The_file.ownerPCode
    pro_name = project.name
    A = Nodes.objects.all()
    node_objs =[]
    Project = []
    proj_objs = []
    proj_user = []

    for x in A:
        if x.ownerFCode.Code == The_file.Code:
            node_objs.append(x)
            The_File = x.ownerFCode
            Project = x.ownerPCode #나중에 진짜로 연결. 지금은 가라 쳐두기
    json_data = serializers.serialize("json", Nodes.objects.filter(ownerFCode = The_file.Code))

    for x in Profile.objects.all():
        a = x.projects.split(',')
        proj_objs = a
        if pro_name in proj_objs:
            proj_user.append(x.user)
    profiles = []
    for username in proj_user:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        profiles.append(profile)

    return render(request, 'NodeApp/node_list.html',{'proj_obj':proj_obj,'node_objs':node_objs,'The_File':The_File, "json":json_data,"proj_user":profiles})


def node_detail(request,node_Code):
    node_obj = Nodes.objects.filter(Code = node_Code)
    The_file = Nodes.objects.get(Code=node_Code).ownerFCode
    print(The_file,'hi')
    return render(request, 'NodeApp/node_details.html', {'node_obj':node_obj,'The_file':The_file})

def create_node(request):
    IAmNodePk = request.POST['something4']
    NodeParentsFileCode = request.POST['something5']
    redirectURL = '/node/node_list/'+str(NodeParentsFileCode)
    clickedNode = Nodes.objects.get(Code=int(IAmNodePk)) #-->PNODE 
    # nodesInProject = Nodes.objects.filter(Code=int(IAmNodePk)) #--> FNODE
    node_object = Nodes()
    node_object.fileObj = request.FILES['myFile']
    node_object.previousCode = clickedNode
    node_object.ownerFCode = clickedNode.ownerFCode
    node_object.ownerPCode = clickedNode.ownerPCode
    node_object.whoIsOwner = request.user
    node_object.save()

    # PNode = Nodes.objects.get(Code=int(pkCode))
    # # 내가누른노드
    # FNode = Nodes.objects.filter(Code=int(pkCode))
    # # 타겟노드
    # The_file = PNode.ownerFCode
    

    # if request.method == 'POST':
    #     pk = request.POST['pk']
    #     next_url = '/node/node_list/'+str(pk)
    #     node_obj = Nodes()
    #     # 새로생긴node_obj
    #     node_obj.fileObj = request.FILES['myFile']
    #     node_obj.previousCode = PNode
    #     node_obj.ownerFCode = PNode.ownerFCode
    #     node_obj.ownerPCode = PNode.ownerPCode
    #     node_obj.whoIsOwner = request.user
    #     node_obj.save()

    #     return redirect(next_url)
    # else:
    return redirect(redirectURL)
    # return render(request,'NodeApp/node_list.html')
    # {'FNode':FNode,'The_file':The_file}

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

    
def changeNodeInfo(request):
    return render(request,'NodeApp/node_list.html')
