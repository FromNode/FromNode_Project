import os
import random
from collections import Counter


def contribution(proj_user,total_node,total_comment,project_pk):
    
    result = {}

    for user in proj_user:

        user_node_num = user.dashboard_user_set.get(project=project_pk).nodes
        # 유저별 노드 수
        similarity_aver = user.dashboard_user_set.get(project=project_pk).contribution
        # 유저별 유사도 평균
        user_comment = user.dashboard_user_set.get(project=project_pk).comments
        # 유저별 코멘트 수

        how_contribute = [0.9,0.1]
        # node와 comment의 기여도 정도

        node_contribute = (user_node_num/total_node)*(similarity_aver/10)*how_contribute[0]
        comment_contribute = (user_comment/total_comment)*how_contribute[1]
        # 노드 기여도, 코멘트 기여도 계산

        result[user.username] = round(node_contribute +comment_contribute,2)*100
        # 최종 결과

    print(result)
    return result 

def communication_frequency(proj_user,total_comment,project_pk):
    result = {}

    for user in proj_user:
        user_comment = user.dashboard_user_set.get(project=project_pk).comments
        result[user.username] = (user_comment/total_comment)*100

    print(result)
    return result

def node_upload_distribution(project,total_node):

    node_time_term = [0,0,0,0]

    nodes = total_node.order_by('createdDate')
    first_time_node = nodes[0]
    first_time = first_time_node.createdDate

    nodes = total_node.order_by('-createdDate')
    last_time_node = nodes[0]
    last_time = last_time_node.createdDate


    time_gap = (last_time - first_time)/4

    for node in nodes:
        if node.createdDate<=first_time+time_gap:
            node_time_term[0] += 1
        elif first_time+time_gap < node.createdDate <= first_time+time_gap*2:
            node_time_term[1] += 1
        elif first_time+time_gap*2 < node.createdDate <= first_time+time_gap*3:
            node_time_term[2] += 1
        else:
            node_time_term[3] += 1
    print(node_time_term,last_time)
    return node_time_term, last_time


