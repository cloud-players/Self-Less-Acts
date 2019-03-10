from django.db import models
import django
import datetime
from django.conf import settings 

# Create your models here.
class user(models.Model):
	"""docstring for user"""
	username = models.CharField(max_length = 400, primary_key = True)
	password = models.CharField(max_length = 42)

	def __str__(self):
		return "%s" %(self.username)
