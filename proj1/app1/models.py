from django.db import models
from datetime import datetime,timedelta,date
# Create your models here.
user_choices = [
	('Librarian','Librarian'),
	('Student','Student'),
]
requested_status = [
	('Booked','Booked'),
	('To Be Returned','To be Returned'),
	('Returned','Returned'),
]
class User(models.Model):
	name = models.CharField(max_length=50)
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=50)
	contact = models.CharField(max_length=50)
	user_type = models.CharField(max_length=10,choices = user_choices,default='Librarian')
	def __str__(self):
		return self.name

class books(models.Model):
	name = models.CharField(max_length=50)
	author = models.CharField(max_length=50)
	no_of_copies = models.IntegerField()
	summary = models.CharField(max_length=300,default = 'default')
	subject = models.CharField(max_length=50,default = 'subject')
	star_rating = models.IntegerField(default = 1)
	def __str__(self):
		return self.name + " " + self.author + " " + str(self.no_of_copies)
class requested(models.Model):
	name = models.CharField(max_length=50)
	requestedBy = models.CharField(max_length=50)
	status = models.CharField(max_length=50,choices = requested_status,default='Booked')
	issue_date = models.DateField(default= date.today())
	return_date = models.DateField(default = date.today()+timedelta(days=7))
	def __str__(self):
		return self.name + " " + self.requestedBy
