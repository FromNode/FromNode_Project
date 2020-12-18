from django.shortcuts import render, redirect
from .models import Nodes
from FileApp.models import Files
from ProjectApp.models import Projects
from django.contrib.auth.models import User
from datetime import datetime
from django.core import serializers
from UserApp.models import Profile

def get_location_list(dbData):
    #str타입 리스트 만들기
    li_numMentioned =[]
    num_mentioned = 0
    node_count = 1
    for obj in dbData:
        if obj.previousCode == None:
            li_numMentioned.append([obj.Code, num_mentioned, obj.previousCode, node_count])
            node_count += 1
        else:
            li_numMentioned.append([obj.Code, num_mentioned, obj.previousCode.Code, node_count])
            node_count += 1
    

    #노드별 브랜치 파생 여부 구하기(언급횟수 구하기)
    for i in range(0,len(li_numMentioned)):
        search_target = li_numMentioned[i][0] #자 내 코드는 이것이다
        searched_men_num = 0
        for j in range(i,len(li_numMentioned)): #다른애들의 previous와 내 코드를 비교해보아라
            if li_numMentioned[j][2] == search_target:
                searched_men_num += 1
                li_numMentioned[i][1] = searched_men_num
    
    #배치시작
    li_last = []
    li_temp = []
    li_location = [] #최종으로 넘겨줄 노드 좌표리스트. [x넘버(열번호),브랜치넘버(행번호),노드코드] 로 저장됨
    is_started = False
    for n, node in enumerate(li_numMentioned):
        print("지금 배치할것이 머냐면 " + node[0])
        print("누구 뒤냐면 " + str(node[2]))
        if is_started == False: #첫 노드
            print("첫 노드 찾았다")
            li_temp.append([node[0]])
            li_last.append(node[0])
            is_started = True
        else:
            if node[2] in li_last: #따라갈 놈이 끝놈이면
                print("따라갈 놈이 있네")
                for i, sublist in enumerate(li_temp):
                    if node[2] in sublist: #내 앞에놈이 있는 행에 추가하자
                        li_temp[i].append(node[0])
                        break
                for k, endnode in enumerate(li_last):
                    if endnode == node[2]:
                        print("끝놈정보에 내껄로 업뎃할게" + node[0])
                        li_last[k] = node[0]
                        break
            else: #새 브랜치 생성해야 되면 순서 파악 후에 그 위치에 생성
                for i, sublist in enumerate(li_temp):
                    if node[2] in sublist:
                        li_temp.insert(i+1, [node[0]])
                        li_last.insert(i+1,node[0])
                        break

    num_of_branch = len(li_temp)
    
    for y, sublist in enumerate(li_temp):
        for node in sublist:
            code = node
            for i in range(0,len(li_numMentioned)):
                if li_numMentioned[i][0] == code:
                    xLoc = li_numMentioned[i][3]
                    li_location.append([xLoc, y+1, code])
                    break
    
    print(li_location)
    print(li_last)
    return li_location, num_of_branch, node_count




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
    user_data = serializers.serialize("json", User.objects.all())
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

    if True:
        dbData = Nodes.objects.filter(ownerFCode = The_file.Code)
        tuple_return = get_location_list(dbData)
        li_location = tuple_return[0]
        num_of_row = tuple_return[1]
        num_of_column = tuple_return[2] 

    gridRowWidth = "100px "
    gridColumnHeight = "100px "
    gridRowNum = gridRowWidth * num_of_row
    gridColumnNum = gridColumnHeight * num_of_column

    objects = {
        'li_location':li_location,
        'gridRowNum':gridRowNum,
        'gridColumnNum':gridColumnNum,
        'num_of_row':num_of_row, 
        'num_of_column':num_of_column, 
        'proj_obj':proj_obj,
        'node_objs':node_objs,
        'The_File':The_File, 
        'json':json_data,
        'proj_user':profiles}  
    return render(request, 'NodeApp/test.html', objects)

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

# def Upload(request):
#     nodeobj = Nodes()
#     nodeobj.Code = "001000"
#     nodeobj.createdDate = datetime.now
#     for files in request.FILES.getlist('myFile'):
#          nodeobj.fileObj = files
#     nodeobj.previousCode =Nodes.objects.get(Code="000001") 
#     nodeobj.ownerPCode = Projects.objects.get(Code="000001")
#     nodeobj.whoIsOwner = User.objects.get(username = 'sea')
#     nodeobj.save()
    
#     return render(request, 'NodeApp/version_all.html')

def CreateTree(request, file_Code):
    The_file = Files.objects.get(Code=file_Code)
    json_data = serializers.serialize("json", Nodes.objects.filter(ownerFCode = The_file.Code))
    # temp = []
    gridRowWidth = "100px "
    gridColumnHeight = "100px "
    gridRowNum = gridRowWidth * 5
    gridColumnNum = gridColumnHeight * 5
    objects = {
        'gridRowNum':gridRowNum, 
        'gridColumnNum':gridColumnNum,
        'rows' : 5,
        'columns' : 5,
        'json_data' : json_data,
    }
    return render(request, 'NodeApp/test.html', objects)

