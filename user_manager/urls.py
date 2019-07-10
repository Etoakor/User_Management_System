"""user_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,re_path
from app01 import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login.html', views.login),
    path('index.html', views.index),
    path('logout.html', views.logout),
    path('classes.html', views.handle_classes),
    path('add_classes.html', views.handle_add_classes),
    path('edit_classes.html', views.handle_edit_classes),
    path('del_classes.html', views.handle_del_classes),
    path('student.html', views.handle_student),
    path('add_student.html', views.add_student),
    path('edit_student.html', views.edit_student),
    path('teacher.html', views.handle_teacher),
    path('add_teacher.html', views.add_teacher),
    re_path('edit_teacher-(\d+).html', views.edit_teacher),
]
