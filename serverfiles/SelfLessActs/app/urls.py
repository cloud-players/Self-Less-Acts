from django.urls import path

from .views import *

urlpatterns = [
    path('mainpage', mainpage, name='mainpage'),
    #path('categories/<category_name>', disp_category, name='disp_category'),
   	#path('<category_name>/acts/<act_id>', disp_act, name='disp_act'),
   	#path('upload', upload_form, name='upload_form'),

  
   	path('api/v1/users', AddUser, name='AddUser'),
   	path('api/v1/users/<username>', RemoveUser, name='RemoveUser'),
   	path('api/v1/categories', ListAll_Add_Category, name='ListAll_Add_Category'),
   	#path('api/v1/categories', AddCategory, name='AddCategory'),
  	path('api/v1/categories/<categoryName>/acts/size', NumberOfActsInCategory, name='NumberOfActsInCategory'),
  	path('api/v1/categories/<categoryName>/acts', ListActsInCategory, name='ListActsInCategory'),
   	#path('api/v1/categories/<categoryName>/acts?start=<startRange>&end=<endRange>', ListActsInCategoryInRange, name='ListActsInCategoryInRange'),
   	path('api/v1/categories/<categoryName>', RemoveCategory, name='RemoveCategory'),  	
   	path('api/v1/acts/upvote', UpvoteAct, name='UpvoteAct'),
   	path('api/v1/acts/<actId>', RemoveAct, name='RemoveAct'),
   	path('api/v1/acts', UploadAct, name='UploadAct'),
   
   	#path('api/category/list', CategoryList, name='CategoryList'),
   	#path('api/category/add', CategoryAdd, name='CategoryAdd'),
   	#path('api/category/remove', CategoryRemove, name='CategoryRemove'),
]