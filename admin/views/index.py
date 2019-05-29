from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse

from common.models import Users
import time, json

def verify(request):
    import random
    from PIL import Image, ImageDraw, ImageFont
    #bgcolor = (random.randrange(20, 100), random.randrange(
    #    20, 100),100)
    bgcolor = (242,164,247)
    width = 100
    height = 25

    im = Image.new('RGB', (width, height), bgcolor)
    draw = ImageDraw.Draw(im)
    for i in range (0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)

    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    rand_str = ''

    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    font = ImageFont.truetype('static/STXIHEI.TTF', 21)
    # font = ImageFont.load_default().font
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)

    del draw
    request.session['verifycode'] = rand_str
    import io
    buf = io.BytesIO()
    im.save(buf, 'png')
    return HttpResponse(buf.getvalue(), 'image/png')


def login(request):
    return render(request, 'admin/login.html')

def dologin(request):
    verify_code = request.session['verifycode']
    code = request.POST['code']
    if verify_code != code:
        context = {'info': '验证码错误'}
        return render(request, "admin/login.html", context)
    try:
        user = Users.objects.get(username=request.POST['username'])
        if user.state == 0:
            import hashlib
            m = hashlib.md5()
            m.update(bytes(request.POST['password'], encoding="utf8"))
            if user.password == m.hexdigest():
                request.session['adminuser'] = user.name
                return HttpResponseRedirect(reverse('admin_index'))
            else:
                context = {'info': '登录密码错误'}
        else:
            context = {'info': '非后台管理用户'}
    except:
        context = {'info': '登录账号错误'}
    return render(request, 'admin/login.html', context)

def logout(request):
    del request.session['adminuser']
    return HttpResponseRedirect(reverse('admin_login'))

def index(request):
    '''管理后台首页'''
    return render(request, "admin/index.html")

