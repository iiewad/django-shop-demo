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
from admin.views import index, users

urlpatterns = [
    path('', index.index, name="admin_index"),

    path('users/', users.index, name="admin_users_index"),
    path('users/add/', users.add, name="admin_users_add"),
    path('users/insert/', users.insert, name="admin_users_insert"),
    path('users/del/<int:uid>/', users.delete, name="admin_users_delete"),
    path('users/edit/<int:uid>/', users.edit, name="admin_users_edit"),
    path('users/update/<int:uid>/', users.update, name="admin_users_update"),
]
