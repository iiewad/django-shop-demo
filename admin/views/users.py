from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator

from common.models import Users
from datetime import datetime


def updatepw(request, uid):
    try:
        ob = Users.objects.get(id=uid)
        if request.POST['password'] != request.POST['repeat-password']:
            context = {'info': '密码不匹配'}
        else:
            import hashlib
            m = hashlib.md5()
            m.update(bytes(request.POST['password'], encoding="utf8"))
            ob.password = m.hexdigest()
            ob.save()
            context = {'info': '密码重置成功'}
    except Exception as err:
        print(err)
        context = {'info': '密码重置失败'}
    return render(request, 'admin/info.html', context)

def resetpw(request, uid):
    try:
        #ob = Users.objects.values_list('username', 'name')
        ob = Users.objects.get(id=uid)
        context = {'user': ob}
        return render(request, 'admin/users/resetpw.html', context)
    except Exception as err:
        print(err)
        context = {'info': 'No Objects'}
    return render(request, 'admin/info.html', context)

def index(request, pIndex):
    # sexlist = Users.objects.values('sex').distinct()
   
    mod = Users.objects
    mywhere = []
    kw = request.GET.get("keyword", None)
    sexid = request.GET.get("sexid", None)
    list = mod.order_by("username")

    if kw:
        list = list.filter(username__contains=kw)
        mywhere.append("keyword="+kw)
    
    if sexid:
        list = list.filter(sex=sexid)
        mywhere.append("sexid="+sexid)
    

    pIndex = int(pIndex)
    page = Paginator(list, 5)
    maxpages = page.num_pages
    
    if pIndex > maxpages:
        page = maxpages
    if pIndex < maxpages:
        pIndex = 1
    
    list2 = page.page(pIndex)
    plist = page.page_range

    context = {
        'userslist': list2,
        'plist': plist,
        'pIndex': pIndex,
        'maxpages': maxpages,
        'mywhere': mywhere
    }

    return render(request, 'admin/users/index.html', context)
    

    """
    list = Users.objects.all()
    context = { "userslist": list }
    return render(request, 'admin/users/index.html', context)
    """

def add(request):
    return render(request, 'admin/users/add.html')

def insert(request):
    try:
        ob = Users()
        ob.username = request.POST['username']
        ob.name = request.POST['name']

        import hashlib
        m = hashlib.md5()
        m.update(bytes(request.POST['password'], encoding="utf8"))
        ob.password = m.hexdigest()
        ob.sex = request.POST['sex']
        ob.address = request.POST['address']
        ob.code = request.POST['code']
        ob.phone = request.POST['phone']
        ob.email = request.POST['email']
        ob.state = 1
        ob.addtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': "添加成功" }
    except Exception as err:
        print(err)
        context = { 'info': "添加失败" }
    
    return render(request, 'admin/info.html', context)

def delete(request, uid):
    try:
        ob = Users.objects.get(id=uid)
        ob.delete()
        context = {'info':'删除成功！'}
    except:
        context = {'info':'删除失败！'}
    return render(request,"admin/info.html",context)

def edit(request, uid):
    try:
        ob = Users.objects.get(id=uid)
        context = {'user': ob}
        return render(request, 'admin/users/edit.html', context)
    except Exception as err:
        print(err)
        context = {'info': '没有找到要修改的信息'}
    return render(request, 'admin/info.html', context)

def update(request, uid):
    try:
        ob = Users.objects.get(id=uid)
        ob.name = request.POST['name']
        ob.sex = request.POST['sex']
        ob.address = request.POST['address']
        ob.code = request.POST['code']
        ob.phone = request.POST['phone']
        ob.email = request.POST['email']
        ob.state = request.POST['state']
        ob.save()
        context = {'info':'修改成功！'}
    except Exception as err:
        print(err)
        context = {'info':'修改失败！'}
    return render(request,"admin/info.html",context)
