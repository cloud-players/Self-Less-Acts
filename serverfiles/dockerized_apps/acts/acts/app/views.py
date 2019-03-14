from . import models
import base64
from django.conf.urls.static import static
import os
from dateutil.parser import parse
 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import *
import json
import requests

#user_service_ip = "http://localhost:8080"

def dt_tm(dt, s2o=None, o2s=None):
	print(dt)
	if s2o == True:
		dt = dt[:10]+" "+dt[17:19]+":"+dt[14:16]+":"+dt[11:13]
		print(dt)
		return parse(dt)
	if o2s == True:
		return dt.strftime("%d-%m-%Y:%S-%M-%H")



@api_view(['GET', 'POST'])
def ListAll_Add_Category(request):
	#to list all the categories
	if request.method == "GET":
		print("\nListAllCategory :", request.data, "\n")

		od = dict()
		for i in models.category.objects.all():
			od[i.categoryName] = i.categoryCount
			
		if len(od) == 0:
			return Response({}, status=HTTP_204_NO_CONTENT)
			
		return Response(od, status=HTTP_200_OK)

	#to add a category
	elif request.method == 'POST':
		data = request.data
		print("\nAddCategory :", data, "\n")	
		
		try:
			if len(data[0]) == 0:
				return Response({}, status=HTTP_400_BAD_REQUEST)
			
			models.category.objects.create(categoryName=data[0])
			return Response({}, status=HTTP_201_CREATED)
			
		except Exception as e:
				print("Exception :", e)
				return Response({}, status=HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def RemoveCategory(request, categoryName):
	data = request.data
	print("\nRemove category :", data, "\n")	
	
	try:
		ps = models.category.objects.get(pk=categoryName).delete()
		return Response({}, status=HTTP_200_OK)

	except Exception as e:
		print("Exception :", e)
		return Response({}, status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def ListActsInCategory(request, categoryName, *args, **kwargs):
	print("\nListActs :", request.data, "\n")	
	
	try:
		category = models.category.objects.get(pk = categoryName)
		startRange, endRange = request.GET.get('start'), request.GET.get('end')

		if category.categoryCount >= 100:
			return Response({}, status=HTTP_413_REQUEST_ENTITY_TOO_LARGE)
		
		if category.categoryCount == 0 or len(request.data) != 0:
			return Response([], status=HTTP_204_NO_CONTENT)

		li = []
		for i in models.act.objects.filter(categoryName=categoryName).order_by('-timestamp'):
			od = dict()	
			od['actId'] = i.actId
			od['username'] = i.username
			od['timestamp'] = dt_tm(i.timestamp, o2s=True)
			od['caption'] = i.caption
			od['upvotes'] = i.upvotes
			od['imgB64'] = i.imgB64
			li.append(od)
		
		#if no range is specified in the url
		if startRange == None or endRange == None:
			return Response(li, status=HTTP_200_OK)			
		
		#if range in specified in the url
		else:
			if int(endRange) - int(startRange) + 1 > 100:
				return Response({}, status=HTTP_413_REQUEST_ENTITY_TOO_LARGE)
			
			if int(endRange) <= 0 or int(startRange) <= 0 or int(endRange) > category.categoryCount:
				return Response({}, status=HTTP_400_BAD_REQUEST)

			return Response(li[int(startRange):int(endRange)+1], status=HTTP_200_OK)

	except Exception as e:
		print("Exception :", e)
		return Response({}, status=HTTP_204_NO_CONTENT)


@api_view(['GET'])
def NumberOfActsInCategory(request, categoryName):
	print("\n NumberOfActsInCategory :", request.data, "\n")	
	
	try:
		category = models.category.objects.get(pk = categoryName)
		return Response([category.categoryCount], status=HTTP_200_OK)
	
	except Exception as e:
		return Response([], status=HTTP_204_NO_CONTENT)


@api_view(['POST'])
def UpvoteAct(request):
	data = request.data
	print("\n UpvoteAct :", data, "\n")	
	
	if not isinstance(data[0], int):
		return Response({}, status=HTTP_400_BAD_REQUEST)
	
	try:	
		p = models.act.objects.get(pk = data[0])
		p.upvotes += 1
		p.save()
		return Response([], status=HTTP_200_OK)
	
	except Exception as e:
		print("Exception :", e)
		return Response({}, status=HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def RemoveAct(request, actId):
	data = request.data
	print("\nRemoveAct :", data, "\n")	
	
	try:
		p = models.act.objects.get(pk = int(actId))
		p.categoryName.categoryCount -= 1
		p.categoryName.save()
		p.delete()
		return Response({}, status=HTTP_200_OK)
	
	except Exception as e:
		print("Exception :", e)
		return Response({}, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def UploadAct(request):
	data = request.data
	print("\nUploadActs :", data, "\n")	

	#user validation
	try:
		users = requests.get("http://172.17.0.3:80/api/v1/users","{}").text
	except requests.exceptions.ConnectionError:
		print("ConnectionError")
		return Response({}, status = HTTP_400_BAD_REQUEST)
	
	try:
		if data["username"] not in users:
			print("username not found in", users)
			return Response({}, status = HTTP_400_BAD_REQUEST)
	except Exception as e:	
		print("Exception :", e)
		return Response({}, status=HTTP_400_BAD_REQUEST)
	
	try:
		#base 64 string validation
		if base64.b64encode(base64.b64decode(data['imgB64'])).decode() != data['imgB64']:
			return Response({}, status=HTTP_400_BAD_REQUEST)
		if not isinstance(data['actId'], int) or 'upvotes' in data:
			return Response({}, status = HTTP_400_BAD_REQUEST)

		formatted_timestamp = dt_tm(data['timestamp'], s2o=True)
		categoryName = models.category.objects.get(pk=data['categoryName'])
		c = models.act.objects.create(actId=int(data['actId']), username=data["username"], timestamp=formatted_timestamp, caption=data['caption'], categoryName=categoryName, imgB64=data['imgB64'])
		c.categoryName.categoryCount += 1
		c.categoryName.save()
		return Response({}, status=HTTP_201_CREATED)
	
	except Exception as e:	
		print("Exception :", e)
		return Response({}, status=HTTP_400_BAD_REQUEST)

'''
{
"actId": 1234,
"username": "john_doe",
"timestamp": "23-12-2323:45-34-22",
"caption": "caption text",
"categoryName": "cat1",
"imgB64": "bGlmZSBpcyBncmVhdA=="
}
'''

'''
curl --header "Content-Type: application/json" \
	--request POST \
	--data '{"actId": 1234, "username": "john_doe", "timestamp": "23-12-2323:45-34
-22", "caption": "caption text", "categoryName": "cat1", "imgB64": "bGlm
ZSBpcyBncmVhdA=="}' \
	http://172.17.0.3:80/api/v1/users
'''