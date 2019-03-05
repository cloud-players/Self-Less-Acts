from django.db import models
import django
import datetime
from django.conf import settings 

# Create your models here.
class category(models.Model):
	"""docstring for category"""
	categoryName = models.CharField(max_length=50, primary_key=True)
	categoryCount = models.IntegerField(default=0)
	def __str__(self):
		return "%s" %(self.categoryName)

class user(models.Model):
	"""docstring for user"""
	username = models.CharField(max_length = 400, primary_key = True)
	password = models.CharField(max_length = 42)

	def __str__(self):
		return "%s" %(self.username)

class act(models.Model):
	"""docstring for Act"""
	actId = models.IntegerField(primary_key=True)
	username = models.ForeignKey(user, default='johndoe==', on_delete=models.SET_DEFAULT)
	timestamp = models.DateTimeField(default=django.utils.timezone.now)
	caption = models.CharField(max_length=200)
	upvotes = models.IntegerField(default=0)
	imgB64 = models.CharField(max_length=1000)
	categoryName = models.ForeignKey(category, on_delete=models.CASCADE)


	def __str__(self):
		return "%d, %s, %s" %(self.actId, self.imgB64, self.caption)
