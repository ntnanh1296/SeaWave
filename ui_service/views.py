from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm, PostForm
from django.contrib import messages
import firebase_admin
from firebase_admin import storage, credentials
from .forms import PostForm, CommentForm
from post_service.models import Post, Comment, PostLike, CommentLike
from post_service.serializers import PostSerializer, CommentSerializer, PostLikeSerializer, CommentLikeSerializer
from user_service.models import CustomUser
from rest_framework import viewsets
from django.views import View
from django.views.generic.edit import FormMixin
from django.views.generic import ListView
from django.urls import reverse_lazy

cred = credentials.Certificate('firebase_credentials.json')
try:
    firebase_admin.initialize_app(cred, name='SeaWave')
except ValueError as e:
    messages.error("Error initializing Firebase app: %s", e)

# Firebase Storage bucket name
BUCKET_NAME = 'seawave-d58e4.appspot.com'

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class PostLikeViewSet(viewsets.ModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer


class CommentLikeViewSet(viewsets.ModelViewSet):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer

class UserPostList(View):
    def get(self, request, username):
        user = get_object_or_404(CustomUser, username=username)
        posts = Post.objects.filter(author=user)
        context = {'user': user, 'posts': posts}
        # return render(request, 'app_main/user_post_list.html', context)

class PostList(FormMixin, ListView):
    model = Post
    template_name = 'ui_service/home.html'
    context_object_name = 'posts'
    ordering = '-create_at'
    form_class = PostForm
    success_url = reverse_lazy('home')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     posts = context['posts']
    #     for post in posts:
    #         if post.media_url:
    #             post.get_media_url = post.media_url.replace('https://storage.googleapis.com/moonland-99249.appspot.com/post_media/', 'https://firebasestorage.googleapis.com/v0/b/moonland-99249.appspot.com/o/post_media%2F') 
    #             post.get_media_url = post.get_media_url + '?alt=media'
    #         post.author = post.author
    #     context['posts'] = posts
    #     return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class PostDetailView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comment_form = CommentForm()
        comments = post.comments.all() 
        return render(request, 'ui_service/post_detail.html', {'post': post, 'comment_form': comment_form, 'comments': comments})

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post-detail', pk=pk)

        comments = post.comments.all()
        return render(request, 'ui_service/post-post_detail.html', {'post': post, 'comment_form': comment_form, 'comments': comments})

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

def update_media(post, file):
    if post.media_url:
        blob = storage.bucket(BUCKET_NAME).blob(post.media_url)
        blob.delete()

    bucket = storage.bucket(BUCKET_NAME)
    blob = bucket.blob('post_media/' + file.name)
    file.seek(0)  # Ensure the file is at the beginning
    blob.upload_from_file(file, content_type='image/jpeg')  # Set the content type to image/jpeg
    blob.make_public()
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

@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author or request.user.is_superuser:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return redirect('post-detail', pk=pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'ui_service/edit_post.html', {'form': form})
    else:
        return HttpResponseForbidden()

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author or request.user.is_superuser:
        if request.method == 'POST':
            post.delete()
            return redirect('post-list')
        return render(request, 'ui_service/delete_post.html', {'post': post})
    else:
        return HttpResponseForbidden()


@login_required
def create_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.user_id = request.user.id
            comment.save()
            return redirect('post-detail', pk=pk)
    else:
        comment_form = CommentForm()
    
    return render(request, 'ui_service/post_detail.html', {'post': post, 'comment_form': comment_form})

@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.user != comment.author:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post-detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'ui_service/edit_comment.html', {'form': form, 'comment': comment})

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.user != comment.author:
        return HttpResponseForbidden()

    if request.method == 'POST':
        post_id = comment.post.id  # Get the post PK before deleting the comment
        comment.delete()
        return redirect('home', pk=post_id)

    return render(request, 'app_main/delete_comment.html', {'comment': comment})
    
@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.postLikes.filter(user=request.user).exists():
        post.postLikes.filter(user=request.user).delete()
        is_liked = False
    else:
        PostLike.objects.create(user=request.user, post=post)
        is_liked = True

    post.like_count = post.postLikes.count()
    post.save()

    return JsonResponse({'like_count': post.like_count, 'is_liked': is_liked})


@login_required
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if comment.commentLikes.filter(user=request.user).exists():
        comment.commentLikes.filter(user=request.user).delete()
        is_liked = False
    else:
        CommentLike.objects.create(user=request.user, comment=comment)
        is_liked = True
        
    comment.like_count = comment.commentLikes.count()
    comment.save()

    return JsonResponse({'like_count': comment.like_count, 'is_liked': is_liked})

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

    if request.user.is_authenticated:
        
        # post_list_view = PostList()
        # post_list_view.request = request
        # post_list_view.args = ()  # Set args and kwargs as needed
        # post_list_view.kwargs = {}

        posts = Post.objects.all().order_by('-created_at')

        # Render the template with the posts
        return render(request, 'ui_service/home.html', {'form': form, 'posts': posts})
        
    return render(request, 'ui_service/home.html', {'form': form})