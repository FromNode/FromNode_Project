import json
import logging
import mimetypes
import os
import urllib
from datetime import datetime

from django.contrib.auth.models import User
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from FileApp.models import Files
from ProjectApp.models import Projects
from UserApp.models import Profile

from NodeApp.forms import CommentForm
from NodeApp.similarity.similarity import (similarity_compare,
                                           similarity_sentence_compare)
from NodeApp.summarization.summary import summary
from NodeApp.textualization.convert import convert, get_str, docx_read
from NodeApp.similarity.vector_similarity import cosine_similarity_compare

from docx import Document
import docx

from .models import Node_Comment, Nodes


def filter_axis(child_list, x_value, y_value, coordinate_node_test, i_dict, check):

    if child_list == []:
        if len(coordinate_node_test) == 20:
            return
        else:
            pass
            # y_value
    else:
        x_value += 1
        for child in child_list:

            coordinate_node_test.append([x_value, y_value, child])
            child_list = i_dict.get(child)

            filter_axis(child_list, x_value, y_value,
                        coordinate_node_test, i_dict, check)
            y_value += 1
        is_first = True

    return coordinate_node_test


def get_location_list(dbData):
    # str타입 리스트 만들기
    li_test = []
    for obj in dbData:
        if obj.previousCode == None:
            li_test.append([obj.Code, obj.previousCode, obj.createdDate])
        else:
            li_test.append([obj.Code, obj.previousCode.Code, obj.createdDate])
    i_dict = {}
    first_node_code = ''
    print(li_test)
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
    check = False
    child_list = ''
    coordinate_node_test = []
    x_value = 1
    y_value = 1

    coordinate_node_test.append([x_value, y_value, first_node_code])
    child_list = i_dict.get(first_node_code)
    last = filter_axis(child_list, x_value, y_value, coordinate_node_test, i_dict, check)
    x_save = 'first'
    ch = 0
    max_x = max([x[0] for x in last])

    for i in range(1, max_x+1):
        last_same_x = [x for x in last if x[0] == i]

        for n, i in enumerate(last_same_x):
            if n == 0:
                pass
            else:
                y_pre = last_same_x[n-1][1]
                y_now = last_same_x[n][1]
                if y_now <= y_pre:
                    last_same_x[n][1] = y_pre+1

    max_y = max([x[1] for x in last])
    li_location = last
    num_of_row = max_y+2
    num_of_column = max_x+2
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
    print(li_location)
    return li_location, num_of_row, num_of_column, coordinates


# def node_list(request, file_Code):
#     if request.user.is_authenticated:
#         Users = request.user
#         unliked_proj = Users.Joined_Unliked_Projects.all()
#         liked_proj = Users.Joined_Liked_Projects.all()
#         all_proj = unliked_proj.union(liked_proj)
#         proj_obj = all_proj
#         # 로그인 한 유저가 포함된 Project를 역참조로 불러옵니다.
#         The_File = Files.objects.get(Code=file_Code)
#         project = The_File.ownerPCode
#         pro_name = project.name
#         node_objs = The_File.File_Nodes.all()
#         proj_user = project.unliked_members.all().union(project.liked_members.all())
#         # 유저가 누른 File에 해당하는 Objects들을 The_File로 불러옵니다.
#         # project는 File이 속한 project
#         # pro_name은 그 project의 이름
#         # node_objs는 file에 속한 노드 전체
#         for i in proj_user:
#             print(i.Profile)
#         # print(project_members.Profile)
#         json_data = serializers.serialize("json", node_objs)
#         # Node에 정보를 담기 위한 데이터를 불러옴

#         tuple_return = get_location_list(node_objs)
#         li_location = tuple_return[0]
#         num_of_row = tuple_return[1]
#         num_of_column = tuple_return[2]

#         gridRowWidth = "100px "
#         gridColumnHeight = "100px "
#         gridRowNum = gridRowWidth * num_of_row
#         gridColumnNum = gridColumnHeight * num_of_column
#         # Html로 전송할 정보들

#         comments = Node_Comment.objects.all()
#         form = CommentForm()
#     else:
#         pass

def node_list(request, proj_Code):
    if request.user.is_authenticated:
        Users = request.user
        unliked_proj = Users.Joined_Unliked_Projects.all()
        liked_proj = Users.Joined_Liked_Projects.all()
        all_proj = unliked_proj.union(liked_proj)
        proj_obj = all_proj
        # 로그인 한 유저가 포함된 Project를 역참조로 불러옵니다.
        project = Projects.objects.get(Code=proj_Code)
        node_objs =project.Proj_Nodes.all()
        pro_name = project.name
        pro_code = proj_Code
        proj_user = project.unliked_members.all().union(project.liked_members.all())
        # 유저가 누른 File에 해당하는 Objects들을 The_File로 불러옵니다.
        # project는 File이 속한 project
        # pro_name은 그 project의 이름
        # node_objs는 file에 속한 노드 전체
        json_data = serializers.serialize("json", node_objs)
        # Node에 정보를 담기 위한 데이터를 불러옴

        all_node_data = []
        for i in range(0, len(node_objs)):
            all_node_data.append(
                {
                    # 노드 이름, 날짜, pk, 주인 유저의 색
                    'node_name': str(node_objs[i].comment),
                    'created_date': str(node_objs[i].createdDate.strftime("%Y.%m.%d")),
                    'node_code': str(node_objs[i].Code),
                    'owner_color': node_objs[i].whoIsOwner.Profile.user_color
                }
            )
        all_node_data_to_json = json.dumps(all_node_data, ensure_ascii=False)
        # print(all_node_data_to_json)
        if node_objs:
            tuple_return = get_location_list(node_objs)
        else:
            tuple_return = [0,0,0,0]
        li_location = tuple_return[0]
        num_of_row = tuple_return[1]
        num_of_column = tuple_return[2]
        coordinates = tuple_return[3]
        gridRowWidth = "100px "
        gridColumnHeight = "200px "
        gridRowNum = gridRowWidth * num_of_row
        gridColumnNum = gridColumnHeight * num_of_column
        
    if request.method == "POST":
        node_comment_create(request, proj_Code)

    if json_data == '[]':
        empty_check = ''
    else:
        empty_check = 'none'

    objects = {
        "li_location": li_location,
        "gridRowNum": gridRowNum,
        "gridColumnNum": gridColumnNum,
        # 함수 get_location_list의 결과물, li_location은 노드가 들어갈 grid의 위치
        # RowNum과 ColumnNum은 들어가는 노드 정보 변동에 따라 Grid 크기 조절
        "num_of_row": num_of_row,
        "num_of_column": num_of_column,
        # 행과 열의 개수를 넘김
        "proj_obj": proj_obj,
        "node_objs": node_objs,
        "json": json_data,
        "proj_user": proj_user,
        "pro_name": pro_name,
        "coordinates": coordinates,
        "all_node_data_to_json": all_node_data_to_json,
        'empty_check':empty_check,
        'pro_code':pro_code,
    }
    # print(json_data)
    return render(request, 'NodeApp/node_list.html', objects)


def node_comment_create(request, proj_Code):
    if request.method == "POST":
        node_comment_create(request, proj_Code)

    objects = {
        "li_location": li_location,
        "gridRowNum": gridRowNum,
        "gridColumnNum": gridColumnNum,
        # 함수 get_location_list의 결과물, li_location은 노드가 들어갈 grid의 위치
        # RowNum과 ColumnNum은 들어가는 노드 정보 변동에 따라 Grid 크기 조절
        "num_of_row": num_of_row,
        "num_of_column": num_of_column,
        # 행과 열의 개수를 넘김
        "proj_obj": proj_obj,
        "node_objs": node_objs,
        "The_File": The_File,
        "json": json_data,
        "proj_user": proj_user,
        "pro_name": pro_name,

        "comments": comments,
        'form': form,
    }

    return render(request, 'NodeApp/node_list.html', objects)


def node_detail(request, node_Code):
    node_obj = Nodes.objects.filter(Code=node_Code)
    The_file = Nodes.objects.get(Code=node_Code).ownerPCode
    node_comments = Node_Comment.objects.filter(node_code=node_Code)
    node_code = Nodes.objects.get(Code=node_Code).Code

    # 멘션 가능한 프로젝트 팀원들
    project_code = Nodes.objects.get(Code=node_Code).ownerPCode
    # print(project_code)
    members = project_code.unliked_members.all().union(
        project_code.liked_members.all())
    # print(members)

    member_list = serializers.serialize('json', members)
    return render(request, 'NodeApp/node_details.html', {'node_obj': node_obj, 'The_file': The_file, 'node_comments': node_comments, 'node_code': node_code})

# json으로 멘션 가능한 멤버 data 보내기


def mentionable_member_json(request):
    # if request.method == 'POST':
    #     request_data = request.POST.get('code',None)
    #     print(request_data)
    # # json_data = json.loads(request.body)
    # print(json_data)

    # # node_code = request.POST['node_code']
    # node_code = request.GET.get('code')
    # print(node_code)

    # if request.method == 'POST':
    #     json_data = json.loads(request.body)
    #     node_code = json_data['code']
    #     print(node_code)

    data = [{'key': 'Peter', 'value': 'Peter123'},
            {'key': 'Julia', 'value': 'Julia38'}]

    return JsonResponse(data, safe=False)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author_comment = request.user
            comment.create_date = timezone.now()
            comment.node_Code = node_Code
            comment.node_code_id = node_Code
            redirectURL = '/node/node_list/'+file_Code
            comment.save()
            return redirect(redirectURL)
    else:
        pass
        # form = CommentForm()
    # context = {'form': form}
    return redirect(redirectURL)


def comment_submit(request):
    node_pk = request.POST['node_pk']
    mentioned_name = request.POST['mentioned_name']  # Profile.nickname
    comment_text = request.POST['comment_text']
    comment_author = request.user.Profile.nickname  # Profile.nickname
    author_profile = request.user.Profile.profile_image.url
    # print(node_pk)
    # print(mentioned_name)
    # print(comment_text)
    # print(comment_author)
    # member=User.objects.get(username=mentioned_name)
    # print(member)
    if mentioned_name != "":
        # 멘션된 사람 있으면
        cmt_obj = Node_Comment()
        cmt_obj.node_code = Nodes.objects.get(Code=node_pk)
        cmt_obj.author_comment = request.user  # Save as User model
        cmt_obj.content = comment_text
        cmt_obj.create_date = timezone.now()
        mentioned_member_Profile = Profile.objects.get(nickname=mentioned_name)
        cmt_obj.who_is_mentioned = mentioned_member_Profile.user  # Save as User model
        cmt_obj.save()
        data = {'author_img': author_profile,
                'comment_author': comment_author,  # nickname
                'create_date': cmt_obj.create_date.strftime("%Y-%m-%d %p %I:%M"),
                'mentioned_name': '@'+mentioned_name,  # nickname
                'content': comment_text
                }

    else:
        # 멘션된 사람 없으면
        cmt_obj = Node_Comment()
        cmt_obj.node_code = Nodes.objects.get(Code=node_pk)
        cmt_obj.author_comment = request.user
        cmt_obj.content = comment_text
        cmt_obj.create_date = timezone.now()
        cmt_obj.who_is_mentioned = None
        cmt_obj.save()
        data = {'author_img': author_profile,
                'comment_author': comment_author,  # nickname
                'create_date': cmt_obj.create_date.strftime("%Y-%m-%d %p %I:%M"),
                'mentioned_name': "",
                'content': comment_text
                }

    # print(data)

    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json")


def load_comment(request):
    node_pk = request.POST['node_pk']
    comments = Node_Comment.objects.filter(node_code=node_pk)
    comment_data = []
    for i in range(0, len(comments)):
        if comments[i].who_is_mentioned != None:

            comment_data.append(
                {'node_code': str(comments[i].node_code),
                'content': str(comments[i].content),
                'author': str(comments[i].author_comment),
                'author_img_url': str(comments[i].author_comment.Profile.profile_image.url),
                'created_date': comments[i].create_date.strftime("%Y-%m-%d %p %I:%M"),
                'who_is_mentioned': '@'+str(comments[i].who_is_mentioned.Profile.nickname)
                }
            )
        else:
            comment_data.append(
                {'node_code': str(comments[i].node_code),
                'content': str(comments[i].content),
                'author': str(comments[i].author_comment.Profile.nickname),
                'author_img_url': str(comments[i].author_comment.Profile.profile_image.url),
                'created_date': comments[i].create_date.strftime("%Y-%m-%d %p %I:%M"),
                'who_is_mentioned': ""
                }
            )    
        # print(comment_data)
    data = json.dumps(comment_data, ensure_ascii=False)
    return JsonResponse(data, safe=False)


def node_detail(request, node_Code):
    node_obj = Nodes.objects.filter(Code=node_Code)
    The_file = Nodes.objects.get(Code=node_Code).ownerFCode

    return render(request, 'NodeApp/node_details.html', {'node_obj': node_obj, 'The_file': The_file})


def create_node(request):
    # 냐아

    # 나중에 쓰일 수도 ? 클릭한 노드 정보 일단 담아뒀음
    # NodeComment = request.POST['NodeComment']
    # NodeComment = 'Test'
    # NodeCreatedDate = request.POST['NodeCreatedDate']
    # NodeDescription = request.POST['NodeDescription']
    # NodeFileObj = request.POST['NodeFileObj']
    # NodeName = request.POST['NodeName']
    # NodeOwnerFileCode = request.POST['NodeOwnerFileCode']
    # NodeOwnerProjectCode = request.POST['NodeOwnerProjectCode']
    # NodePreviousCode = request.POST['NodePreviousCode']
    # NodeOwner = request.POST['NodeOwner']
    # NodePk = request.POST['NodePk']
    # redirectURL = '/node/node_list/'+str(NodeOwnerFileCode)

    # 파일없을 때 예외 처리 해야합니다
    if request.method == 'POST':
        nodePk = request.POST['this_node_pk']
        print(nodePk)
        PCode = request.POST['ownerPCode']
        node_obj = Nodes()
        if nodePk == '':
            # first node

            # docx_read 함수를 통해 현재 업로드 되는 Docx File의 txt 추출 후 description 필드에 txt str 삽입
            if request.FILES['uploadFile'].name.split(".")[-1] == "docx":
                document = docx.Document(request.FILES['uploadFile'])
                file_txt = docx_read(document)
            else:
                file_txt = "파일 없음"
            node_obj.description = file_txt

            node_obj.fileObj = request.FILES['uploadFile']
            node_obj.filename = request.FILES['uploadFile'].name
            node_obj.ownerPCode = Projects.objects.get(Code = PCode)
            node_obj.comment = request.POST['node_name']
            node_obj.whoIsOwner = request.user
            node_obj.save()
            proj_obj = Projects.objects.get(Code=PCode)
            proj_obj.Proj_Nodes.add(node_obj)
            proj_obj.save()

            redirectURL = '/node/node_list/'+str(PCode)
        else:
            clickedNode = Nodes.objects.get(Code=str(nodePk))
            print(clickedNode,'안녕')
            redirectURL = '/node/node_list/'+str(PCode)


        # # Summary Part 미사용으로 일시 보존
        # # Start Summary part
        #     # File 확장자 확인, docx인가?
        #     # 현재 summary/convert 대상 확장자 docx이므로 docx에 한정, 추후 판단을 위한 사용자정의 function 사용 고려
        #     if request.FILES['uploadFile'].name.split(".")[-1] == "docx" and clickedNode.filename.split(".")[-1] == "docx":
        #         # temp_summary_file 변수에 convert된 Object 담기
        #         temp_summary_file = convert(request.FILES['uploadFile'])
        #         # convert된 문서 object를 get_str 함수를 통해 String화
        #         temp_summary_file_str = get_str(temp_summary_file)
        #         # summary 함수로 String화 된 문서 Object를 요약하여 str_summary 변수에 담기
        #         str_summary = summary(temp_summary_file_str)
        #         # description 필드에 요약된 Text 삽입

        #         # 유사도 결과물 넣을 Empty_list 생성
        #         similarity_list = []
        #         previous_node_file = clickedNode.fileObj
        #         previous_node_file = convert(previous_node_file)
        #         # Similarity Module 사용하여 유사도 비교
        #         similarity_sentence_compare(previous_node_file,
        #                         temp_summary_file, "temp_user", similarity_list)
        #         # similarity와 summary text 저장
        #         node_obj.similarity = 100 - similarity_list[4]
        #         node_obj.description = str_summary

        #         # 추가한 글자수와 라인수를 저장
        #         node_obj.added_letters = similarity_list[5]
        #         node_obj.added_sentences = similarity_list[6]

        #         # 기존 Project File에 해당하는지 or 기타 File인지 판단
        #         if 100 - similarity_list[4] > 5:  # 5% 이상의 유사도를 가진 File이며, docx 확장자에 해당하는 File
        #             node_obj.is_workflow = 1  # Project File로 판단하여 1 삽입
        #         else:
        #             node_obj.is_workflow = 0
        #     else:  # docx 외의 File
        #         node_obj.is_workflow = 0
        #     # End Summary part 

            # docx_read 함수를 통해 현재 업로드 되는 Docx File의 txt 추출 후 description 필드에 txt str 삽입
            if request.FILES['uploadFile'].name.split(".")[-1] == "docx":
                document = docx.Document(request.FILES['uploadFile'])
                file_txt = docx_read(document)
            else:
                file_txt = "파일 없음"
            node_obj.description = file_txt

            # Start Similarity Part
            previous_node_file_txt = clickedNode.description
            similarity_value = cosine_similarity_compare(file_txt, previous_node_file_txt)
            node_obj.similarity = similarity_value
            # End Similarity Part

            node_obj.fileObj = request.FILES['uploadFile']
            node_obj.filename = request.FILES['uploadFile'].name
            node_obj.previousCode = clickedNode
            node_obj.ownerPCode = clickedNode.ownerPCode
            node_obj.whoIsOwner = request.user
            node_obj.comment = request.POST['node_name']
            node_obj.save()
            proj_obj = Projects.objects.get(Code=PCode)
            proj_obj.Proj_Nodes.add(node_obj)
            proj_obj.save()
            return redirect(redirectURL)
    return redirect(redirectURL)


def changeNodeInfo(request):
    return render(request, 'NodeApp/node_list.html')


def download_view(request, pk):
    node = get_object_or_404(Nodes, Code=pk)
    url = node.fileObj.url[1:]
    file_url = urllib.parse.unquote(url)
    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            quote_file_url = urllib.parse.quote(node.filename.encode('utf-8'))
            response = HttpResponse(
                fh.read(), content_type=mimetypes.guess_type(file_url)[0])
            response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
            return response
        raise Http404


def load_node_data(request):
    node_pk = request.POST['node_pk']
    target_node = Nodes.objects.get(Code=node_pk)
    # Node 모델에 있는거 싹 다 가지고 옵시다 !
    created_date = target_node.createdDate  # : 노드가 생긴 시간
    fileObj = target_node.fileObj  # : 노드에 업로드 된 첨부파일
    filename = target_node.filename
    previousCode = target_node.previousCode
    ownerPCode = target_node.ownerPCode
    whoIsOwner = target_node.whoIsOwner  # : 노드 올린 사람
    comment = target_node.comment  # : actually 노드 이름입니다.
    similarity = target_node.similarity  # : 유사도
    description = target_node.description  # : Node의 File의 txt 데이터
    is_workflow = target_node.is_workflow # : workflow에서 작업하던 파일이니?
    added_letters = target_node.added_letters # : text 몇개가 추가됐니?

    owner_profile = whoIsOwner.Profile.profile_image.url  # : 유저 프로필 사진
    owner_nickname = whoIsOwner.Profile.nickname  # : 유저 닉네임
    owner_color = whoIsOwner.Profile.user_color

    data = {'node_name': comment,
            'created_date': created_date.strftime("%Y-%m-%d %p %I:%M"),
            'author_color': owner_color,
            'author_nickname': owner_nickname,
            'description': description,
            'similarity': similarity,
            'is_workflow':is_workflow,
            'added_letters':added_letters
            }

    # print(data)
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json")

