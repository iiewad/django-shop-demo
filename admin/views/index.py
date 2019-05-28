from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    '''管理后台首页'''
    return render(request, "admin/index.html")
