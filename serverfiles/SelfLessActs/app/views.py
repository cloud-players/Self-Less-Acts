from django.shortcuts import render
from . import models
import base64
from django.conf.urls.static import static
import os
from dateutil.parser import parse
 
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import *
from django.http import JsonResponse
from collections import OrderedDict
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def dt_tm(dt, s2o=None, o2s=None):
	print(dt)
	if s2o == True:
		dt = dt[:10]+" "+dt[17:19]+":"+dt[14:16]+":"+dt[11:13]
		print(dt)
		return parse(dt)
	if o2s == True:
		return dt.strftime("%d-%m-%Y:%S-%M-%H")


@api_view(['POST'])
def AddUser(request):
	if request.method == 'POST':
		data = request.data
		print("\nAddUser :", data, "\n")	

		if type(data['password']) != str or len(data['password']) != 40 or len(data['username']) == 0:
			return Response({}, status=HTTP_400_BAD_REQUEST)

		try:
			#to check if it is in hexdigest
			int(data['password'], 16)
			c = models.user.objects.create(username=data['username'], password=data['password'])
			return Response({}, status=HTTP_201_CREATED)
		except Exception as e:
			print("Exception :", e)
			return Response({}, status=HTTP_400_BAD_REQUEST)
	else:
		return Response({}, status=HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['DELETE'])
def RemoveUser(request, username):
	if request.method == 'DELETE':
		data = request.data
		print("\nRemoveUser :", data, "\n")	

		try:
			models.user.objects.get(pk = username).delete()
			return Response({}, status=HTTP_200_OK)
		except Exception as e:
			print("Exception :", e)
			return Response({}, status=HTTP_400_BAD_REQUEST)
	else:
		return Response({}, status=HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST'])
def ListAll_Add_Category(request):
	if request.method == "GET":
		print("\nListAllCategory :", request.data, "\n")

		od = dict()
		categorys = models.category.objects.all()
		for i in categorys:
			od[i.name] = i.count
		
		if len(od) == 0:
			return Response({}, status=HTTP_204_NO_CONTENT)
		
		return Response(od, status=HTTP_200_OK)

	elif request.method == 'POST':
		data = request.data
		print("\nAddCategory :", data, "\n")	
		if len(data[0]) == 0:
			return Response({}, status=HTTP_400_BAD_REQUEST)
		try:
			models.category.objects.create(name=data[0])
			cwd = os.getcwd()
			os.chdir(BASE_DIR+'/static/imgs')
			os.mkdir(data[0])
			os.chdir(cwd)
			return Response({}, status=HTTP_201_CREATED)
		except Exception as e:
			print("Exception :", e)
			return Response({}, status=HTTP_400_BAD_REQUEST)

	else:
		return Response({}, status=HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['DELETE'])
def RemoveCategory(request, categoryName):
	if request.method == 'DELETE':
		data = request.data
		print("\nRemove category :", data, "\n")	

		try:
			ps = models.category.objects.get(pk=categoryName)
			for p in models.act.objects.filter(category=categoryName):
				#p = models.act.objects.get(pk = i.act_id)
				p.category.count -= 1
				p.category.save()
				os.remove(BASE_DIR + p.img_path)
				p.delete()

			cwd = os.getcwd()
			os.chdir(BASE_DIR+'/static/imgs')
			os.rmdir(categoryName)
			os.chdir(cwd)

			ps.delete()
			return Response({}, status=HTTP_200_OK)
		except Exception as e:
			print("Exception :", e)
			return Response({}, status=HTTP_400_BAD_REQUEST)

	else:
		return Response({}, status=HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['GET'])
def ListActsInCategory(request, categoryName, *args, **kwargs):
	if request.method == "GET":
		
		print("\nListActs :", request.data, "\n")	
		try:
			category = models.category.objects.get(pk = categoryName)
		
			if category.count >= 100:
				return Response({}, status=HTTP_413_REQUEST_ENTITY_TOO_LARGE)
			print(category.count, category)
			if category.count == 0 or len(request.data) != 0:
				return Response([], status=HTTP_204_NO_CONTENT)

			li = []
		
			startRange, endRange = request.GET.get('start'), request.GET.get('end')
			if startRange == None or endRange == None:
				for i in models.act.objects.filter(category = categoryName):
					od = dict()	
					od['actId'] = i.act_id
					od['username'] = i.username.username
					od['timestamp'] = dt_tm(i.pub_datetime, o2s=True)
					od['caption'] = i.caption
					od['upvotes'] = i.upvotes
					od['imgB64'] = base64.encodestring(open((BASE_DIR + i.img_path), 'rb').read())
					li.append(od)
			else:
				#print(int(endRange) - int(startRange))
				if int(endRange) - int(startRange) + 1 > 100:
					return Response({}, status=HTTP_413_REQUEST_ENTITY_TOO_LARGE)
				if int(endRange) <= 0 or int(startRange) <= 0 or int(endRange) > category.count:
					return Response({}, status=HTTP_400_BAD_REQUEST)
				for i in models.act.objects.filter(category=categoryName).order_by('-pub_datetime')[int(startRange):int(endRange)+1]:
					od = dict()	
					od['actId'] = i.act_id
					od['username'] = i.username.username
					od['timestamp'] = dt_tm(i.pub_datetime, o2s=True)
					od['caption'] = i.caption
					od['upvotes'] = i.upvotes
					od['imgB64'] = base64.encodestring(open((BASE_DIR + i.img_path), 'rb').read())
					li.append(od)

			return Response(li, status=HTTP_200_OK)

		except Exception as e:
			print("Exception :", e)
			return Response({}, status=HTTP_204_NO_CONTENT)

	else:
		return Response([], status=HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def NumberOfActsInCategory(request, categoryName):
	if request.method == "GET":
		print("\n NumberOfActsInCategory :", request.data, "\n")	
		
		try:
			category = models.category.objects.get(pk = categoryName)
		
			print(category, category.count)
			#if category[0].count == 0:
			#	return Response([], status=HTTP_204_NO_CONTENT)
		
			return Response([category.count], status=HTTP_200_OK)
		except Exception as e:
			return Response([], status=HTTP_204_NO_CONTENT)
	else:
		return Response([], status=HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def UpvoteAct(request):
	if request.method == "POST":
		data = request.data
		print("\n UpvoteAct :", data, "\n")	
		if not isinstance(data[0], int):
			return Response({}, status=HTTP_400_BAD_REQUEST)

		try:	
			p = models.act.objects.get(pk = data[0])
			print(type(p.act_id))
			p.upvotes += 1
			p.save()
			return Response([], status=HTTP_200_OK)
		except Exception as e:
			print("Exception :", e)
			return Response({}, status=HTTP_400_BAD_REQUEST)
	else:
		return Response([], status=HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['DELETE'])
def RemoveAct(request, actId):
	if request.method == "DELETE":
		data = request.data
		print("\nRemoveAct :", data, "\n")	
		
		try:
			p = models.act.objects.get(pk = int(actId))
			p.category.count -= 1
			p.category.save()

			os.remove(BASE_DIR + p.img_path)
			p.delete()
			return Response({}, status=HTTP_200_OK)

		except Exception as e:
			print("Exception :", e)
			return Response({}, status=HTTP_400_BAD_REQUEST)
	else:
		return Response({}, status=HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def UploadAct(request):
	if request.method == 'POST':
		data = request.data
		
		print("\nUploadActs :", data, "\n")	
		try:
			if base64.b64encode(base64.b64decode(data['imgB64'])).decode() != data['imgB64']:
				return Response({}, status=HTTP_400_BAD_REQUEST)
			if not isinstance(data['actId'], int) or 'upvotes' in data:
                        	return Response({}, status = HTTP_400_BAD_REQUEST)
		except Exception as e:	
			print(e)
			return Response({}, status=HTTP_400_BAD_REQUEST)
			
		try:
			dt_tm(data['timestamp'], s2o=True)
			category = models.category.objects.get(pk=data['categoryName'])
			username = models.user.objects.get(pk=data['username'])
			img_path = '/static/imgs/'+category.name
			img = base64.standard_b64decode(data['imgB64'].encode())
			#s = base64.decodestring(s.encode())
			print(img)
			c = models.act.objects.create(act_id=int(data['actId']), username=username, pub_datetime=dt_tm(data['timestamp'], s2o=True), caption=data['caption'], category=category, img_path=img_path+'/'+str(data['actId'])+'.jpg')
			c.category.count += 1
			c.category.save()

			cwd = os.getcwd()
			os.chdir(BASE_DIR+img_path)
			#img_path += '/'+str(data['actId'])+'.jpg'
			open((str(data['actId'])+'.jpg'), 'wb').write(img)
			#open((str(data['actId'])+'.jpg'), 'wb').write(s)
			os.chdir(cwd)
			
			return Response({}, status=HTTP_201_CREATED)
		
		except Exception as e:
			print('\n\n\nException :', e, '\n\n\n')
			return Response({}, status=HTTP_400_BAD_REQUEST)
	
	else:
		return Response({}, status=HTTP_405_METHOD_NOT_ALLOWED)

'''
hashlib.sha1('namee'.encode('utf-8')).hexdigest()
@api_view(['GET', 'PUT'])
def CategoryRemovePut(request):
	if request.method == 'PUT':
		data = request.data	
		#print('\n\n', ', '.join(i for i in dir(data) if not i.startswith('__')), '\n\n')
		
		if len(data) != 1 or type(data) != list or type(data[0]) != str or len(data[0]) <= 0:
			return Response(json.dumps({}), status=HTTP_400_BAD_REQUEST)

		#print('\n\n', type(data), type(data[0]), '\n\n')
		if models.category.objects.filter(name = data[0]).count() == 0:
			return Response(json.dumps({}), status=HTTP_400_BAD_REQUEST)

		#print('\n\n', data, '\n\n')
		models.category.objects.get(pk=data[0]).delete()
		#c = models.category.objects.create(name=data[0])
		return Response(json.dumps({}), status=HTTP_200_OK)
	
	else:
		return Response(json.dumps({}), status=HTTP_405_METHOD_NOT_ALLOWED)
'''

# Create your views here.
def mainpage(request):
	category_list = models.category.objects.all()
	print(category_list)
	#output = ', '.join([q.question_text for q in latest_question_list])
	context = {'category_list' : category_list}
	return render(request, 'app/mainpage.html', context)
    
'''   
def disp_category(request, category_name):
	act_list = models.act.objects.filter(category=category_name)
	context = {'act_list' : act_list, 'category_name' : category_name}
	for i in act_list:
		print(i.act_id, i.pub_datetime, i.caption, i.upvotes, i.img_path, i.category)
	return render(request, 'app/disp_category.html', context)	

def disp_act(request, category_name, act_id):
	try:
		act = models.act.objects.get(pk=act_id)
	except act.DoesNotExist:
		raise Http404("act does not exist")
	#question = get_object_or_404(Question, pk=question_id)
	pass

def upload_form(request):
	return render(request, 'app/upload.html', None)


def category_list(request):
	categories = models.category.objects.all()
'''
