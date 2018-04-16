"""api URL Configuration

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
from django.urls import path
from django.contrib import admin

import uvigo.views

urlpatterns = [
    path('', uvigo.views.index, name='index'),
    path('admin/', admin.site.urls, name='admin'),
    path('register/', uvigo.views.student_register, name='register'),
    path('login/', uvigo.views.user_login, name='login'),
    path('profile/', uvigo.views.user_profile, name='profile'),
    path('topology/', uvigo.views.topology_data, name='topology'),
    path('indications/', uvigo.views.indications_data, name='indications'),
    path('classrooms/', uvigo.views.classrooms, name='classrooms'),
    path('schedules/', uvigo.views.schedules, name='schedules'),
    path('teachers/', uvigo.views.teachers, name='teachers'),
    path('teachers/register/', uvigo.views.teacher_register, name='teachers-registration'),
    path('admins/register/', uvigo.views.admin_register, name='admins-registration'),
    path('users-list/', uvigo.views.users_list, name='users-list'),
    path('groups/', uvigo.views.groups, name='groups'),
    path('firebase-notification/', uvigo.views.firebase, name='firebase-notification'),
    path('firebase-instance/', uvigo.views.firebase_token, name='firebase-instance'),
]
