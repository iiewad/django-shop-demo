from django.shortcuts import render
from django.http import HttpResponse

def login(request):
    return render(request, 'admin/login.html')

def dologin(request):
    pass

def logout(request):
    pass
    
def index(request):
    '''管理后台首页'''
    return render(request, "admin/index.html")

