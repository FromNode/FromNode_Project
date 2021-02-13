from django.shortcuts import render, redirect, get_object_or_404
from .models import Nodes
from FileApp.models import Files
from ProjectApp.models import Projects
from django.contrib.auth.models import User
from datetime import datetime
from django.core import serializers
from UserApp.models import Profile

import urllib
import os
from django.http import HttpResponse, Http404
import mimetypes

def filter_axis(child_list,x_value,y_value,coordinate_node_test,i_dict,check):
    
    if child_list == []:
        if len(coordinate_node_test) == 20:
            return 
        else:
            pass
            # y_value
    else:
        x_value +=1
        for child in child_list:
            
            coordinate_node_test.append([x_value,y_value,child])
            child_list = i_dict.get(child)

            filter_axis(child_list,x_value,y_value,coordinate_node_test,i_dict,check)
            y_value +=1
        is_first = True
    
    return coordinate_node_test

def get_location_list(dbData):
    #str타입 리스트 만들기
    li_test = []
    for obj in dbData:
        if obj.previousCode == None:
            li_test.append([obj.Code,obj.previousCode, obj.createdDate])
        else:
            li_test.append([obj.Code,obj.previousCode.Code, obj.createdDate])
    i_dict = {}
    first_node_code = ''

    for i in li_test:
        if i[1] == None:
            first_node_code = i[0]
        i_list = []
        target = i[0]
        for obj in li_test:
            if target == obj[1]:
                # print(obj[0])
                i_list.append(obj[0])
        i_dict[target] = i_list
    check =False
    child_list = ''
    coordinate_node_test = []
    x_value = 1
    y_value = 1

    coordinate_node_test.append([x_value,y_value,first_node_code])
    child_list = i_dict.get(first_node_code)
    last = filter_axis(child_list,x_value,y_value,coordinate_node_test,i_dict,check)
    x_save = 'first'
    ch = 0
    max_x = max([x[0] for x in last])
    
    for i in range(1,max_x+1):
        last_same_x = [x for x in last if x[0]==i]
        
        for n, i in enumerate(last_same_x):
            if n==0:
                pass
            else:
                y_pre = last_same_x[n-1][1]
                y_now = last_same_x[n][1]
                if y_now<=y_pre:
                    last_same_x[n][1] = y_pre+1

    max_y = max([x[1] for x in last])
    li_location = last
    num_of_row = max_x+2
    num_of_column = max_y+2

    coordinates = []

    for node in last:
        start_axis = node[0], node[1]
        child_node = i_dict.get(node[2])
        for child in child_node:
            for i in last:
                if child in i:
                    end_axis = i[0], i[1], 'x'
                    append_axis = start_axis + end_axis
            coordinates.append(append_axis)

    return li_location, num_of_row, num_of_column, coordinates

def node_list(request,file_Code):
    if request.user.is_authenticated:
        Users = request.user
        unliked_proj = Users.Joined_Unliked_Projects.all()
        liked_proj = Users.Joined_Liked_Projects.all()
        all_proj = unliked_proj.union(liked_proj) 
        proj_obj = all_proj
        # 로그인 한 유저가 포함된 Project를 역참조로 불러옵니다.
        The_File = Files.objects.get(Code=file_Code)
        project = The_File.ownerPCode
        pro_name = project.name
        node_objs = The_File.File_Nodes.all()
        proj_user = project.unliked_members.all().union(project.liked_members.all()) 
        # 유저가 누른 File에 해당하는 Objects들을 The_File로 불러옵니다.
        # project는 File이 속한 project
        # pro_name은 그 project의 이름
        # node_objs는 file에 속한 노드 전체
        # print(project_members.Profile)
        json_data = serializers.serialize("json", node_objs)
        # Node에 정보를 담기 위한 데이터를 불러옴

        tuple_return = get_location_list(node_objs)
        li_location = tuple_return[0]
        num_of_row = tuple_return[1]
        num_of_column = tuple_return[2] 
        coordinates = tuple_return[3]
        gridRowWidth = "100px "
        gridColumnHeight = "200px "
        gridRowNum = gridRowWidth * num_of_row
        gridColumnNum = gridColumnHeight * num_of_column
        #Html로 전송할 정보들



    else:
        pass
    
    

    
    objects = {
        "li_location":li_location,
        "gridRowNum":gridRowNum,
        "gridColumnNum":gridColumnNum,
        # 함수 get_location_list의 결과물, li_location은 노드가 들어갈 grid의 위치
        # RowNum과 ColumnNum은 들어가는 노드 정보 변동에 따라 Grid 크기 조절
        "num_of_row":num_of_row, 
        "num_of_column":num_of_column, 
        # 행과 열의 개수를 넘김
        "proj_obj":proj_obj,
        "node_objs":node_objs,
        "The_File":The_File, 
        "json":json_data,
        "proj_user":proj_user,
        "pro_name" : pro_name,
        "coordinates" : coordinates,
    }  
    return render(request, 'NodeApp/node_list.html', objects)

def node_detail(request,node_Code):
    node_obj = Nodes.objects.filter(Code = node_Code)
    The_file = Nodes.objects.get(Code=node_Code).ownerFCode

    return render(request, 'NodeApp/node_details.html', {'node_obj':node_obj,'The_file':The_file})

def create_node(request):
    # 나중에 쓰일 수도 ? 클릭한 노드 정보 일단 담아뒀음
    # NodeComment = request.POST['NodeComment']
    NodeComment = 'Test'
    NodeCreatedDate = request.POST['NodeCreatedDate']
    NodeDescription = request.POST['NodeDescription']
    NodeFileObj = request.POST['NodeFileObj']
    NodeName = request.POST['NodeName']
    NodeOwnerFileCode = request.POST['NodeOwnerFileCode']
    NodeOwnerProjectCode = request.POST['NodeOwnerProjectCode']
    NodePreviousCode = request.POST['NodePreviousCode']
    NodeOwner = request.POST['NodeOwner']
    NodePk = request.POST['NodePk']
    redirectURL = '/node/node_list/'+str(NodeOwnerFileCode)
    
    clickedNode = Nodes.objects.get(Code=str(NodePk))
    print(request.user)
    # 파일없을 때 예외 처리 해야합니다
    if request.method == 'POST':
        node_object = Nodes()
        node_object.fileObj = request.FILES['uploadFile']
        node_object.filename = request.FILES['uploadFile'].name
        node_object.previousCode = clickedNode
        node_object.ownerFCode = clickedNode.ownerFCode
        node_object.ownerPCode = clickedNode.ownerPCode
        node_object.whoIsOwner = request.user
        node_object.save()
        file_object = Files.objects.get(Code = NodeOwnerFileCode)
        file_object.File_Nodes.add(node_object)
        file_object.save()
        return redirect(redirectURL)
    return redirect(redirectURL)

def changeNodeInfo(request):
    return render(request, 'NodeApp/node_list.html')
        
# notice/views.py




def download_view(request, pk):
    node = get_object_or_404(Nodes, Code=pk)
    url = node.fileObj.url[1:]
    file_url = urllib.parse.unquote(url)
    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            quote_file_url = urllib.parse.quote(node.filename.encode('utf-8'))
            response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_url)[0])
            response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
            return response
        raise Http404