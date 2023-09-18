from django.shortcuts import render,redirect
from .models import User
from django.contrib.auth import authenticate,login,logout


def resgister_user(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = User.objects.create_user(username=username,password=password)
		user.save()
		return redirect('login')

	context = {}
	return render(request,'signup.html',context)



def login_user(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username,password=password)
		if user:
			login(request,user)
			return redirect('index')

	context = {}
	return render(request,'registration/login.html',context)



def logout_user(request):
	logout(request)
	return redirect("index")