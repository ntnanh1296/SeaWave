from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm, PostForm
from django.contrib import messages
import firebase_admin
from firebase_admin import storage, credentials

cred = credentials.Certificate('firebase_credentials.json')
try:
    firebase_admin.initialize_app(cred, name='MoonLand')
except ValueError as e:
    messages.error("Error initializing Firebase app: %s", e)

# Firebase Storage bucket name
BUCKET_NAME = 'moonland-99249.appspot.com'

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
                return render(request, 'ui_service/home.html', {'form': form})
            else:
                messages.error(request, 'Invalid username or password')  # Add an error message
    else:
        form = LoginForm()
    return render(request, 'ui_service/home.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')  

def home(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to post list page
            else:
                messages.error(request, 'Invalid username or password')  # Add an error message
    else:
        form = LoginForm()
    return render(request, 'ui_service/home.html', {'form': form})

def update_media(post, file):
    if post.media_url:
        blob = storage.bucket(BUCKET_NAME).blob(post.media_url)
        blob.delete()

    bucket = storage.bucket(BUCKET_NAME)
    blob = bucket.blob('post_media/' + file.name)
    file.seek(0)  # Ensure the file is at the beginning
    blob.upload_from_file(file, content_type='image/jpeg')  # Set the content type to image/jpeg
    post.media_url = blob.public_url
    post.save()

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            if 'media' in request.FILES:
                media_file = request.FILES['media']
                try:
                    update_media(post, media_file)
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
                
                return redirect('home')
            
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
            
    else:
        form = PostForm()

    return redirect('home')


