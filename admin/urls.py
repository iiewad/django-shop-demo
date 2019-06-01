"""django_shop_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from admin.views import index, users, type, goods

urlpatterns = [
    path("goods/<int:pIndex>/", goods.index, name="admin_goods_index"),
    # path('goods/', goods.index, name="admin_goods_index"),
    path("goods/add/", goods.add, name="admin_goods_add"),
    path("goods/insert/", goods.insert, name="admin_goods_insert"),
    path("goods/del/<int:gid>/", goods.delete, name="admin_goods_del"),
    path("goods/edit/<int:gid>/", goods.edit, name="admin_goods_edit"),
    path("goods/update/<int:gid>/", goods.update, name="admin_goods_update"),

    path('type', type.index, name="admin_type_index"),
    path('type/add/<int:tid>/', type.add, name="admin_type_add"),
    path('type/insert/', type.insert, name="admin_type_insert"),
    path('type/del/<int:tid>/', type.delete, name="admin_type_del"),
    path('type/edit/<int:tid>/', type.edit, name="admin_type_edit"),
    path('type/update/<int:tid>/', type.update, name="admin_type_update"),

    path('verify', index.verify, name="admin_verify"),
    path('login', index.login, name="admin_login"),
    path('dologin', index.dologin, name="admin_dologin"),
    path('logout', index.logout, name="admin_logout"),

    path('users/updatepw/<int:uid>/', users.updatepw, name="admin_users_updatepw"),
    path('users/resetpw/<int:uid>/', users.resetpw, name="admin_users_resetpw"),
    path('users/<int:pIndex>/', users.index, name="admin_users_index"),
    path('users/add/', users.add, name="admin_users_add"),
    path('users/insert/', users.insert, name="admin_users_insert"),
    path('users/del/<int:uid>/', users.delete, name="admin_users_delete"),
    path('users/edit/<int:uid>/', users.edit, name="admin_users_edit"),
    path('users/update/<int:uid>/', users.update, name="admin_users_update"),

    path('', index.index, name="admin_index"),

]
