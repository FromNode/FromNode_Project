from django.shortcuts import render, redirect
from .models import Nodes
from django.contrib.auth.models import User

def version_all(request):
    node_obj = Nodes.objects.all()
    return render(request, 'NodeApp/version_all.html', {'node_obj':node_obj})


def node_detail(request):
    return render(request, 'NodeApp/node_detail.html')

def test(request):
    return render(request, 'NodeApp/test.html')