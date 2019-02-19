from django.db import models
import django
import datetime
from django.conf import settings 

# Create your models here.
class category(models.Model):
	"""docstring for category"""
	name = models.CharField(max_length=50, primary_key=True)
	count = models.IntegerField(default=0)
	def __str__(self):
		return "%s" %(self.name)

class user(models.Model):
	"""docstring for user"""
	username = models.CharField(max_length = 400, primary_key = True)
	password = models.CharField(max_length = 42)

	def __str__(self):
		return "%s" %(self.username)

class act(models.Model):
	"""docstring for Act"""
	act_id = models.IntegerField(primary_key=True)
	username = models.ForeignKey(user, default='johndoe', on_delete=models.SET_DEFAULT)
	pub_datetime = models.DateTimeField(default=django.utils.timezone.now)
	caption = models.CharField(max_length=200)
	upvotes = models.IntegerField(default=0)
	img_path = models.CharField(max_length=200)
	category = models.ForeignKey(category, on_delete=models.CASCADE)


	def __str__(self):
		return "%d, %s, %s" %(self.act_id, self.img_path, self.caption)