from django.shortcuts import render, redirect, get_object_or_404
from .models import Nodes, Node_Comment
from FileApp.models import Files
from ProjectApp.models import Projects
from django.contrib.auth.models import User
from datetime import datetime
from django.core import serializers
from UserApp.models import Profile
from NodeApp.forms import CommentForm
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder

import urllib
import os
from django.http import HttpResponse, Http404
import mimetypes


def get_location_list(dbData):
    # str타입 리스트 만들기
    li_numMentioned = []
    num_mentioned = 0
    node_count = 1
    for obj in dbData:
        if obj.previousCode == None:
            li_numMentioned.append(
                [obj.Code, num_mentioned, obj.previousCode, node_count, obj.createdDate])
            node_count += 1
            # print("node storing started" + str(obj.Code) + " " + str(obj.previousCode))
        else:
            li_numMentioned.append(
                [obj.Code, num_mentioned, obj.previousCode.Code, node_count, obj.createdDate])
            node_count += 1

    li_numMentioned.sort(key=lambda x: x[4])
    # 노드별 브랜치 파생 여부 구하기(언급횟수 구하기)
    for i in range(0, len(li_numMentioned)):
        search_target = li_numMentioned[i][0]  # 자 내 코드는 이것이다
        searched_men_num = 0
        for j in range(i, len(li_numMentioned)):  # 다른애들의 previous와 내 코드를 비교해보아라
            if li_numMentioned[j][2] == search_target:
                searched_men_num += 1
                li_numMentioned[i][1] = searched_men_num

    # 배치시작
    li_last = []
    li_temp = []
    li_location = []  # 최종으로 넘겨줄 노드 좌표리스트. [x넘버(열번호),브랜치넘버(행번호),노드코드] 로 저장됨
    is_started = False
    for n, node in enumerate(li_numMentioned):
        if is_started == False:  # 첫 노드
            li_temp.append([node[0]])
            print(li_temp)
            li_last.append(node[0])
            is_started = True
        else:
            if node[2] in li_last:  # 따라갈 놈이 끝놈이면
                for i, sublist in enumerate(li_temp):
                    if node[2] in sublist:  # 내 앞에놈이 있는 행에 추가하자
                        li_temp[i].append(node[0])
                        print(li_temp)
                        break
                for k, endnode in enumerate(li_last):
                    if endnode == node[2]:
                        li_last[k] = node[0]
                        print(li_last)
                        break
            else:  # 새 브랜치 생성해야 되면 순서 파악 후에 그 위치에 생성
                for i, sublist in enumerate(li_temp):
                    if node[2] in sublist:
                        li_temp.insert(i+1, [node[0]])
                        li_last.insert(i+1, node[0])
                        break

    num_of_branch = len(li_temp)

    for y, sublist in enumerate(li_temp):
        for node in sublist:
            code = node
            for i in range(0, len(li_numMentioned)):
                if li_numMentioned[i][0] == code:
                    xLoc = li_numMentioned[i][3]
                    li_location.append([xLoc, y+1, str(code)])
                    break

    # print(li_last)

    # print(li_last)
    # for i in li_location:
    #     print(i)
    return li_location, num_of_branch, node_count


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

def node_list(request, file_Code):
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
        # for i in proj_user:
        #     print(i.Profile)
        # print(project_members.Profile)
        json_data = serializers.serialize("json", node_objs)
        # Node에 정보를 담기 위한 데이터를 불러옴

        tuple_return = get_location_list(node_objs)
        li_location = tuple_return[0]
        num_of_row = tuple_return[1]
        num_of_column = tuple_return[2]

        gridRowWidth = "100px "
        gridColumnHeight = "100px "
        gridRowNum = gridRowWidth * num_of_row
        gridColumnNum = gridColumnHeight * num_of_column
        # Html로 전송할 정보들
        json_set = []
        comment_data = []
        comments = Node_Comment.objects.all()
        for i in range(0, len(comments)):
            if comments[i].who_is_mentioned != None:
                comment_data.append(
                    # [str(comments[i].node_code),
                    # str(comments[i].content),
                    # str(comments[i].author_comment),
                    # str(comments[i].author_comment.Profile.profile_image.url),
                    # str(comments[i].create_date)
                    # ]
                    {'node_code': str(comments[i].node_code),
                     'content': str(comments[i].content),
                     'author': str(comments[i].author_comment.Profile.nickname),
                     'author_img_url': str(comments[i].author_comment.Profile.profile_image.url),
                     'created_date': comments[i].create_date.strftime("%Y-%m-%d %H:%M"),
                     'who_is_mentioned': '@'+str(comments[i].who_is_mentioned.Profile.nickname)
                     }
                )
            else:
                comment_data.append(
                    {'node_code': str(comments[i].node_code),
                     'content': str(comments[i].content),
                     'author': str(comments[i].author_comment.Profile.nickname),
                     'author_img_url': str(comments[i].author_comment.Profile.profile_image.url),
                     'created_date': comments[i].create_date.strftime("%Y-%m-%d %H:%M"),
                     'who_is_mentioned': ""
                     }
                )
        print(comment_data)
        comment_data_to_json = json.dumps(comment_data, ensure_ascii=False)
        # json_set.append(comment_data_to_json)

        # print("냐아", comment_data_to_json)
        # print(comments[0].author_comment.Profile.filter(user_id=comments[0].author_comment.id)[0].name)
        # print(comments[0].author_comment.Profile.profile_image.url)
        # print(comments[0].create_date.strftime("%Y-%m-%d %H:%M"))

        # print("comment_data는??\n",comment_data)
    else:
        pass

    if request.method == "POST":
        node_comment_create(request, file_Code)

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
        "test_comments": comment_data_to_json,
        "comment_data": comment_data,

    }
    return render(request, 'NodeApp/node_list.html', objects)


def node_comment_create(request, file_Code):
    if request.method == "POST":
        node_comment_create(request, file_Code)

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
        'form': form
    }
    return render(request, 'NodeApp/node_list.html', objects)


def node_detail(request, node_Code):
    node_obj = Nodes.objects.filter(Code=node_Code)
    The_file = Nodes.objects.get(Code=node_Code).ownerFCode
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
    mentioned_name = request.POST['mentioned_name']
    comment_text = request.POST['comment_text']
    comment_author = request.user.username
    author_profile = request.user.Profile.profile_image.url
    print(node_pk)
    print(mentioned_name)
    print(comment_text)
    print(comment_author)
    # member=User.objects.get(username=mentioned_name)
    # print(member)
    if mentioned_name != "":
        # 멘션된 사람 있으면
        cmt_obj = Node_Comment()
        cmt_obj.node_code = Nodes.objects.get(Code=node_pk)
        cmt_obj.author_comment = request.user
        cmt_obj.content = comment_text
        cmt_obj.create_date = timezone.now()
        mentioned_member_Profile = Profile.objects.get(nickname=mentioned_name)
        cmt_obj.who_is_mentioned = mentioned_member_Profile.user
        cmt_obj.save()
        data = [{'author_img': author_profile,
                 'comment_author': comment_author,
                 'create_date': cmt_obj.create_date.strftime("%Y-%m-%d %H:%M"),
                 'mentioned_name': comment_author,
                 'content': comment_text
                 }]

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
                'comment_author': comment_author,
                'create_date': cmt_obj.create_date.strftime("%Y-%m-%d %H:%M"),
                'mentioned_name': "",
                'content': comment_text
                }

    print(data)

    # data = {'mentioned_name':mentioned_name,
    #         'comment_text':comment_text}

    # data = [{'comment_text': comment_text,
    #          'author': comment_author,
    #          'create_date' :
    #         {'key': 'Julia', 'value': 'Julia38'}]
    # data = [{'key':'hello'}]
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json")


def load_comment(request):
    node_pk = request.POST['node_pk']
    comments = Node_Comment.objects.filter(node_code=node_pk)
    comment_data = []
    for i in range(0, len(comments)):
        comment_data.append(
            # [str(comments[i].node_code),
            # str(comments[i].content),
            # str(comments[i].author_comment),
            # str(comments[i].author_comment.Profile.profile_image.url),
            # str(comments[i].create_date)
            # ]
            {'node_code': str(comments[i].node_code),
             'content': str(comments[i].content),
             'author': str(comments[i].author_comment),
             'author_img_url': str(comments[i].author_comment.Profile.profile_image.url),
             'created_date': comments[i].create_date.strftime("%Y-%m-%d %H:%M")
             }
        )
        print(comment_data)
    data = json.dumps(comment_data, ensure_ascii=False)
    return JsonResponse(data, safe=False)


def node_detail(request, node_Code):
    node_obj = Nodes.objects.filter(Code=node_Code)
    The_file = Nodes.objects.get(Code=node_Code).ownerFCode

    return render(request, 'NodeApp/node_details.html', {'node_obj': node_obj, 'The_file': The_file})


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
        file_object = Files.objects.get(Code=NodeOwnerFileCode)
        file_object.File_Nodes.add(node_object)
        file_object.save()
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
