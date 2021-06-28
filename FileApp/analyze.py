import os
import random
from collections import Counter


def contribution(proj_user,total_node,total_comment):
    
    result = {}
    total_comment = 0

    for user in proj_user:

        user_node_num = 10 
        # user_node_num = user.dashboard_user.node
        total_node_num = 40
        # total_node_num = len(total_node)
        similarity_aver = 5
        # similarity_aver = user.dashboard_user.similarity
        user_comment = 250
        # user_comment = user.dashboard_user.comments

        total_comment = 1000
        # total_comment = total_comment

        how_contribute = [0.9,0.1]

        node_contribute = (user_node_num/total_node_num)*(similarity_aver/10)*how_contribute[0]
        comment_contribute = (user_comment/total_comment)*how_contribute[1]

        result[user] = node_contribute +comment_contribute

    return result 

def communication_frequency(proj_user,total_comment):
    result = {}

    for user in proj_user:
        user_comment = 250
        # user_comment = user.dashboard_user.comments
        total_comment = 1000
        # total_comment = total_comment

        result[user] = (user_comment/total_comment)*100

    return result

def node_upload_distribution(project):

    node_time_term = [0,0,0,0]
    nodes = project.Proj_Nodes.all()
    first_time_nodes = nodes[0]
    last_time_nodes = nodes[-1]

    time_gap = (last_time_nodes.createDate - first_time_nodes.createDate)/4

    for node in nodes:
        if node.createDate<=first_time_nodes+time_gap:
            node_time_term[0] += 1
        elif first_time_nodes+time_gap < node.createDate <= first_time_nodes+time_gap*2:
            node_time_term[1] += 1
        elif first_time_nodes+time_gap*2 < node.createDate <= first_time_nodes+time_gap*3:
            node_time_term[2] += 1
        else:
            node_time_term[3] += 1

    return node_time_term


