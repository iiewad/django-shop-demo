from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models import Q
from django.core.paginator import Paginator

from common.models import Types, Goods
from PIL import Image
from datetime import datetime
import time,json,os

def index(request, pIndex):
    tlist = Types.objects.extra(select={'_has': 'concat(path, id)'}).order_by('_has')
    for ob in tlist:
        ob.pname = '. . .'*(ob.path.count(',')-1)

    mod = Goods.objects
    mywhere = []

    kw = request.GET.get("keyword", None)
    if kw:
        list = mod.filter(goods__contains=kw)
        mywhere.append("keyword="+kw)
    else:
        list = mod.filter()
    typeid = request.GET.get('typeid', '0')
    if typeid != '0':
        tids = Types.objects.filter(Q(id=typeid) | Q(pid=typeid)).values_list('id', flat=True)
        list = list.filter(typeid__in = tids)
        mywhere.append("typeid=" + typeid)
    state = request.GET.get('state', '')
    if state != '':
        list = list.filter(state = state)
        mywhere.append("state=" + state)

    pIndex = int(pIndex)
    page = Paginator(list, 5)
    maxpages = page.num_pages

    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    
    list2 = page.page(pIndex)
    plist = page.page_range

    for vo in list2:
        ty = Types.objects.get(id=vo.typeid)
        vo.typename = ty.name

    context = {
        'typelist': tlist,
        "goodslist": list2,
        'plist': plist,
        'pIndex': pIndex,
        'maxpages': maxpages,
        'mywhere': mywhere,
        'typeid': int(typeid)
    }

    return render(request, 'admin/goods/index.html', context)

def add(request):
    list = Types.objects.extra(select = {'_has': 'concat(path, id)'}).order_by('_has')
    context = {"typelist": list}
    return render(request, "admin/goods/add.html", context)

def insert(request):
    try:
        myfile = request.FILES.get("pic", None)
        if not myfile:
            return HttpResponse("没有上传信息")

        filename = str(time.time()) + "." +myfile.name.split('.').pop()
        destination = open(os.path.join("./static/goods/", filename), 'wb+')
        for chunk in myfile.chunks():
            destination.write(chunk)
        destination.close()

        im = Image.open("./static/goods/" + filename)
        # rgb_im = im.convert('RGB')
        im.thumbnail((375, 375))
        im.save("./static/goods/" + filename)
        im.thumbnail((220, 220))
        im.save("./static/goods/m_" + filename)
        im.thumbnail((75, 75))
        im.save("./static/goods/s_" + filename)

        ob = Goods()
        ob.goods = request.POST['goods']
        ob.typeid = request.POST['typeid']
        ob.company = request.POST['company']
        ob.price = request.POST['price']
        ob.store = request.POST['store']
        ob.content = request.POST['content']
        ob.picname = filename
        ob.state = 1
        ob.addtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info':'添加成功！'}
    except Exception as err:
        print(err)
        context = {'info':'添加失败！'}

    return render(request,"admin/info.html",context)

def delete(request, gid):
    try:
        ob = Goods.objects.get(id=gid)
        os.remove("./static/goods/" + ob.picname)
        os.remove("./static/goods/m_" + ob.picname)
        os.remove("./static/goods/s_" + ob.picname)
        ob.delete()
        context = {'info': '删除成功'}
    except Exception as err:
        print(err)
        context = {'info': '删除失败'}
    return render(request, 'admin/info.html', context)

def edit(request, gid):
    try:
        ob = Goods.objects.get(id=gid)
        list = Types.objects.extra(select = {'_has': 'concat(path, id)'}).order_by('_has')

        context = {'typelist': list, 'goods': ob}
        return render(request, 'admin/goods/edit.html', context)
    except Exception as err:
        print(err)
        context = {'info': '没有找到要修改的信息'}
    return render(request, 'admin/info.html', context)

def update(request, gid):
    try:
        b = False
        oldpicname = request.POST['oldpicname']
        if None != request.FILES.get("pic"):
            myfile = request.FILES.get("pic")
            if not myfile:
                return HttpResponse("没有上传文件信息")

            filename = str(time.time()) + "." + myfile.name.split('.').pop()
            destination = open(os.path.join("./static/goods/", filename), 'wb+')
            for chunk in myfile.chunks():
                destination.write(chunk)
            destination.close()

            im = Image.open("./static/goods/" + filename)
            im.thumbnail((375, 375))
            im.save("./static/goods/"+filename)
            im.thumbnail((220, 220))
            im.save("./static/goods/m_"+filename)
            im.thumbnail((75, 75))
            im.save("./static/goods/s_"+filename)
            b = True
            picname = filename
        else:
            picname = oldpicname
        
        ob = Goods.objects.get(id = gid)
        ob.goods = request.POST['goods']
        ob.typeid = request.POST['typeid']
        ob.company = request.POST['company']
        ob.price = request.POST['price']
        ob.store = request.POST['store']
        ob.content = request.POST['content']
        ob.picname = picname
        ob.state = request.POST['state']
        ob.save()
        context = {'info':'修改成功！'}
        if b:
            os.remove("./static/goods/m_"+oldpicname) #执行老图片删除  
            os.remove("./static/goods/s_"+oldpicname) #执行老图片删除  
            os.remove("./static/goods/"+oldpicname) #执行老图片删除  
    except Exception as err:
        print(err)
        context = {'info':'修改失败！'}
        if b:
            os.remove("./static/goods/m_"+picname) #执行新图片删除  
            os.remove("./static/goods/s_"+picname) #执行新图片删除  
            os.remove("./static/goods/"+picname) #执行新图片删除  
    return render(request,"admin/info.html",context)



