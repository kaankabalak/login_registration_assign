from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

# Create your views here.
def index(request):
	return render(request, 'first_app/index.html')

def register(request):
	request.session['isLoggedIn'] = False
	postData = {
		'first_name': request.POST['first_name'],
		'last_name': request.POST['last_name'],
		'email': request.POST['email'],
		'password': request.POST['password'],
		'confirm_password': request.POST['password']
	}

	user = User.objects.register(postData)
	request.session['first_name'] = request.POST['first_name']

	print user

	for message in user[1]: # scan the messages
		messages.add_message(request, messages.INFO, message)

	if user[0]:
		return redirect('/success')
	else:
		request.session['isRegistered'] = True
		return redirect('/')

def login(request):
	request.session['isRegistered'] = False
	postData = {
		'email': request.POST['email'],
		'password': request.POST['password'],
	}

	user = User.objects.login(postData)

	for message in user[1]: # scan the messages
		messages.add_message(request, messages.INFO, message)

	print user

	if user[0]:
		request.session['first_name'] = User.objects.get(email=postData['email']).first_name
		messages.add_message(request, messages.INFO, 'Successfully logged in!')
		return redirect('/success')
	else:
		request.session['isLoggedIn'] = True
		return redirect('/')

def success(request):
	context = {
		'users': User.objects.all()
	}
	return render(request, 'first_app/success.html', context)