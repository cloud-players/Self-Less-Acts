"""SelfLessActs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from app.views import *

urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/v1/users', ListAll_Add_User, name='ListAll_Add_User'),
	path('api/v1/users/<username>', RemoveUser, name='RemoveUser'),
	path('api/v1/categories', ListAll_Add_Category, name='ListAll_Add_Category'),
	path('api/v1/categories/<categoryName>/acts/size', NumberOfActsInCategory, name='NumberOfActsInCategory'),
	path('api/v1/categories/<categoryName>/acts', ListActsInCategory, name='ListActsInCategory'),
	path('api/v1/categories/<categoryName>', RemoveCategory, name='RemoveCategory'),  	
	path('api/v1/acts/upvote', UpvoteAct, name='UpvoteAct'),
	path('api/v1/acts/<actId>', RemoveAct, name='RemoveAct'),
	path('api/v1/acts', UploadAct, name='UploadAct')
]