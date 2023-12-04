from django.shortcuts import render, redirect
from user_service.serializers import CustomUser
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'ui_service/register.html', {'form': form})    

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('post-list')  # Redirect to post list page
            else:
                messages.error(request, 'Invalid username or password')  # Add an error message
    else:
        form = LoginForm()
    return render(request, 'ui_service/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')  

def home(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, 'Login Successed')
                # return redirect('post-list')  # Redirect to post list page
            else:
                messages.error(request, 'Invalid username or password')  # Add an error message
    else:
        form = LoginForm()
    return render(request, 'ui_service/home.html', {'form': form})


