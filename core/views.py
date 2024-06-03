from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages 
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request, 'core/home.html');

def register(request):
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password = raw_password)
            login(request, user)
            messages.success(request, "Registration Successful")
            return redirect('login')
        else:
            messages.error(request, "Registration Failed, Please Try Again")
    else:
        form = UserCreationForm()
    return render(request, 'sign_up.html', {'form': form})

def user_login(request):
    if request.method=='POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.data_cleaned.get('username')
            password = form.data_cleaned.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome Back {username}")
                return redirect(None)
            else:
                messages.error("Invalid Username and Password")
        else:
            messages.error("Invalid Username and Password")
    else:
        form = AuthenticationForm()
    return render(request, 'usrs/login.html', {'form':form})

def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('home')



