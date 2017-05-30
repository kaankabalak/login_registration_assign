from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

# Create your models here.
class UserManager(models.Manager):
	salt = bcrypt.gensalt()

	def register(self, postData):
		validation = User.objects.validate(postData)
		if validation[0]:
			User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], password=bcrypt.hashpw(postData['password'].encode(), self.salt))
			message = validation[1]
			return [True, message]
		else: 
			message = validation[1]
			print message
			return [False, message]

	def login(self, postData):
		message = []
		if bcrypt.checkpw(postData['password'].encode(), User.objects.get(email = postData['email']).password.encode() ):
			return [True, message]
		else: 
			message.append('The password is incorrect')
			return [False, message]

	def validate(self, postData):
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		NAME_REGEX = re.compile(r'^[a-zA-Z.+_-]+$')
		isFormValid = True
		message = []
		print User.objects.filter(email=postData['email'])

		if len(postData['first_name']) < 2:
			message.append('First name cannot be less than 2 characters')
			isFormValid = False
		elif not NAME_REGEX.match(postData['first_name']):
			message.append('First name should be letters only')
			isFormValid = False

		if len(postData['last_name']) < 2:
			message.append('Last name cannot be less than 2 characters')
			isFormValid = False
		elif not NAME_REGEX.match(postData['last_name']):
			message.append('Last name should be letters only')
			isFormValid = False

		if len(postData['email']) < 1:
			message.append('Email cannot be empty')
			isFormValid = False
		elif not EMAIL_REGEX.match(postData['email']):
			message.append('Email should be valid')
			isFormValid = False
		elif User.objects.count() != 0 and User.objects.filter(email=postData['email']):
			message.append('This user has already registered')
			isFormValid = False

		if len(postData['password']) < 8:
			message.append('Password cannot be less than 8 characters')
			isFormValid = False
		elif postData['password'] != postData['confirm_password']:
			message.append('Password and password confirmation should match')
			isFormValid = False

		if isFormValid:
			message.append("Thanks for submitting your information")
			return [True, message]
		else:
			return [False, message]

class User(models.Model):
	first_name = models.CharField(max_length=45)
	last_name = models.CharField(max_length=45)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=45)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

	def __unicode__(self):
		return self.first_name + ' ' + self.last_name + ', Email: ' + self.email + ', Password: ' + self.password