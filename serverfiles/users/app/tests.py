#from django.test import TestCase
from json import loads, dumps
# Create your tests here.
import requests
url = 'http://54.91.217.230:8000//api/v1/categories/education/acts'
data = {
		'actId': 1231,
		'username': 'johndoe',
		'timestamp': '2019-02-04T14:50:13Z',
		'caption': 'caption text',
		'imgB64': 'TWFuIGlzIGRpc3Rpbmd1aXNoZWQsIG5vdCBvb',
		'categoryName': 'education'
	}
data = {'username': 'urNam', 'password': '3d725109c7e7c0bfb9d709836735b56d943d263f'}
data = {}
response = requests.get(url, data=dumps(data), headers={"Content-Type": "application/json"})
#response = requests.get(url)
print(response)
print(response.text)