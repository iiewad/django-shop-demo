from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

from common.models import Types


def index(request):
    list = Types.objects.extra(select = {'_has':'concat(path,id)'}).order_by('_has')
    # 遍历查询结果，为每个结果对象追加一个pname属性，目的用于缩进标题
    for ob in list:
        ob.pname ='. . . '*(ob.path.count(',')-1)
        # print(list[0].__dict__)
    context = {"typeslist":list}
    return render(request,'admin/type/index.html',context)


def add(request, tid):
    # 获取父类别信息，若没有则默认为根类别信息
    if tid == 0:
        context = {'pid':0,'path':'0,','name':'根类别'}
    else:
        ob = Types.objects.get(id=tid)
        context = {'pid':ob.id,'path':ob.path+str(ob.id)+',','name':ob.name}
    return render(request,'admin/type/add.html',context)

def insert(request):
    try:
        ob = Types()
        ob.name = request.POST['name']
        ob.pid = request.POST['pid']
        ob.path = request.POST['path']
        ob.save()
        context = {'info': '添加成功'}
    except Exception as err:
        print(err)
        context = {'info': '添加失败'}
    
    return render(request, 'admin/info.html', context)

def delete(request, tid):
    try:
        row = Types.objects.filter(pid=tid).count()
        if row > 0:
            context = {'info': '删除失败: 此类别下有子类'}
            return render(request, 'admin/info.html', context)
        ob = Types.objects.get(id=tid)
        ob.delete()
        context = {'info': '删除成功'}
    except Exception as err:
        print(err)
        context = {'info': '删除失败'}
    return render(request, 'admin/info.html', context)

def edit(request,tid):
    try:
        ob = Types.objects.get(id=tid)
        context = {'type':ob}
        return render(request,"admin/type/edit.html",context)
    except Exception as err:
        print(err)
        context = {'info':'没有找到要修改的信息！'}
    return render(request,"admin/info.html",context)

def update(request, tid):
    try:
        ob = Types.objects.get(id=tid)
        ob.name = request.POST['name']
        ob.save()
        context = {'info': '修改成功'}
    except Exception as err:
        print(err)
        context = {'info': '修改失败'}
    return render(request, 'admin/info.html', context)
