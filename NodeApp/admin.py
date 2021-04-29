from django.contrib import admin

from .models import Node_Comment, Nodes

# admin.site.register(Nodes)
# admin.site.register(Node_Comment)


# 기존 Nodes model의 단순 admin 등록을 대체하는 NodesAdmin Class 정의
# ModelAdmin을 상속받는 형태로 class를 정의하고, list_display에 tuple 형태로 admin 페이지에 표출될 필드를 정의
class NodesAdmin(admin.ModelAdmin):
    list_display = ('Code', 'whoIsOwner',
                    'comment', 'similarity', 'description')


admin.site.register(Nodes, NodesAdmin)


# list_display에서 별도의 필드 정의 없이 모든 필드를 표출하고, 특정 필드를 제외하려면 아래와 같이 작성
class Node_CommentAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Node_Comment._meta.fields if field.name not in ('표출하지 않을 필드 이름')]
    list_display.insert(0, '__str__')


admin.site.register(Node_Comment, Node_CommentAdmin)
