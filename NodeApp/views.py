from django.shortcuts import render, redirect
from .models import Nodes
from FileApp.models import Files
from ProjectApp.models import Projects
from django.contrib.auth.models import User
from datetime import datetime
from django.core import serializers
from UserApp.models import Profile

def get_2D_list(dbData):
    li_numMentioned =[]
    num_mentioned = 0
    is_have_BranchNo = False
    xLoc = 0
    yLoc = 0
    

    #str타입 리스트 만들기
    for obj in dbData:
        if obj.previousCode == None:
            li_numMentioned.append([obj.Code, num_mentioned, obj.previousCode, is_have_BranchNo])
        else:
            li_numMentioned.append([obj.Code, num_mentioned, obj.previousCode.Code, is_have_BranchNo])
    
    #노드별 브랜치 파생 여부 구하기(언급횟수 구하기)
    for i in range(0,len(li_numMentioned)):
        search_target = li_numMentioned[i][0] #자 내 코드는 이것이다
        searched_men_num = 0
        for j in range(i,len(li_numMentioned)): #다른애들의 previous와 내 코드를 비교해보아라
            if li_numMentioned[j][2] == search_target:
                searched_men_num += 1
                li_numMentioned[i][1] = searched_men_num
    
    #행 수, 노드 수 구하기
    num_of_branch = 1
    num_of_node = 0
    for n, row in enumerate(li_numMentioned):
        if row[1] >= 2 :
            num_of_branch += row[1]-1
            num_of_node = n

    li_last = [0 for i in range(num_of_branch)] # 0 0 0
    li_location = []

    
    node_count = 0
    for n, node in enumerate(li_numMentioned):

        check = 0
        for i in range(num_of_branch):
            if li_last[i] == 0:
                check += 1

        #지금 이게 첫 번째 노드인지 확인해서 맞으면 1,1 배정하고 젤끝놈으로 저장
        if check == num_of_branch: #아직 끝놈으로 저장된 게 없으면
            print("나 지금 1번노드 찾았어" + node[0] + "배치중이야")
            node_count += 1
            li_location.append([node_count,1,node[0]])
            li_last[0] = node[0]
            
        #두 번째 노드부터 배치 어떻게 할 건지 시작
        else:
            if node[2] in li_last: #앞놈이 지금 배치된 놈들 중 끝놈이면
                print("나 끝놈들중에 내 previous가 기다리는거 알고있엉 " + node[0] + "배치중이야")
                arranged_branch_YLoc = 0 # 걍 저장용 변수
                for arrangedNode in li_location: #저장된 놈들 중 앞놈의 y정보를 찾자
                    if arrangedNode[2] == node[2]: # 내 앞놈 찾으면
                        node_count += 1
                        li_location.append([node_count,arrangedNode[1],node[0]]) #그대로 가져와서 배치정보로 저장
                        arranged_branch_YLoc = arrangedNode[1] #끝놈저장용 변수에 위치만 저장
                        break
                li_last[arranged_branch_YLoc -1] = node[0]
                print("끝놈리스트의 " + str(arranged_branch_YLoc-1) + " 번 인덱스에다가 " + node[0] + " 로 업데이트합니다")
                print(li_last)

            else: # 앞놈이 끝놈이 아니면
                mentioned_count = 0 #몇 번째 행에 배치할 건지 파악하기 위해서 앞놈의 브랜치개수를 파악
                sum_mentioned_count = 0
                for i in range(0,n):
                    if li_numMentioned[i][1] >= 2:
                        mentioned_count += 1
                        sum_mentioned_count += li_numMentioned[i][1]
                node_count += 1
                li_location.append([node_count, sum_mentioned_count, node[0]])
                li_last[sum_mentioned_count-2] = node[0]
        #브랜치가 복잡해졌을 때의 알고리즘 보완 필요



    li_branch_group = []

    '''
    for i in range(1, num_of_branch): #브랜치별로 그룹을 짤건데 일단 하나씩 파악해볼거야
        li_temp = []
        pointer_temp = 0
        for j in range(len(li_numMentioned),0,-1): #맨 마지막놈부터 보자
            if li_numMentioned[j-1][3] == False: #브랜치 배정이 아직 안된애면
                li_temp.append(li_numMentioned[j-1][0]) #지금 파악중인 그룹에 넣고
                li_numMentioned[j-1][3] = True
                for n, row in enumerate(li_numMentioned): #쟈 이제 걔의 previous를 파보자
                    if row[0] == li_numMentioned[j-1][2]:
                        pointer_temp = n
                while li_numMentioned[pointer_temp][2] == None: #첫노드까지 이 짓을 반복할 거야 이 와일문을 돌면서 브랜치묶음이 완성돼
                    if li_numMentioned[pointer_temp][3] == False:
                        li_temp.append(li_numMentioned[pointer_temp][0])
                        li_numMentioned[pointer_temp][3] = True
                    for n, row in enumerate(li_numMentioned): #쟈 이제 걔의 previous를 파보자
                        if row[0] == li_numMentioned[pointer_temp][2]:
                            pointer_temp = n   
                li_branch_group.append(li_temp)
            else:
                continue
    '''

    
    return li_location, li_last




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

    if True:
        dbData = Nodes.objects.filter(ownerFCode = The_file.Code)
        tuple_return = get_2D_list(dbData)
        li_numMentioned = tuple_return[0]
        num_of_branch = tuple_return[1]
        
    return render(request, 'NodeApp/node_list.html',{'li_numMentioned':li_numMentioned,'num_of_branch':num_of_branch,'proj_obj':proj_obj,'node_objs':node_objs,'The_File':The_File, "json":json_data,"proj_user":profiles})


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
