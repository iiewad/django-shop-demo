from django.shortcuts import redirect
from django.urls import reverse

import re

class ShopMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        urllist = ['/admin/login', '/admin/dologin', '/admin/logout', '/admin/verify']
        path = request.path

        if re.match("/admin", path) and (path not in urllist):
            if "adminuser" not in request.session:
                return redirect(reverse('admin_login'))

        response = self.get_response(request)

        return response