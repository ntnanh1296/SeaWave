from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm, PostForm
from django.contrib import messages
import firebase_admin
from firebase_admin import storage, credentials
from .forms import PostForm, CommentForm, UserProfileForm
from post_service.models import Post, Comment, PostLike, CommentLike
from post_service.serializers import PostSerializer, CommentSerializer, PostLikeSerializer, CommentLikeSerializer
from user_service.models import CustomUser
from rest_framework import viewsets
from django.views import View
from django.views.generic.edit import FormMixin
from django.views.generic import ListView
from django.urls import reverse_lazy
from follow_service.models import Follower
from django.views.generic import TemplateView
from chat_service.models import Chat

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

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class UserProfileView(View):
    def get(self, request, username):
        user = CustomUser.objects.get(username=username)
        posts = Post.objects.filter(author=user)
        follower_count = Follower.objects.filter(user=user).count()
        is_following = Follower.objects.filter(user=user, follower=request.user).exists()
        
        context = {
            'user': user,
            'follower_count': follower_count,
            'is_following': is_following,
            'posts' : posts
        }
        return render(request, 'ui_service/user_profile.html', context)




@login_required
def user_detail(request, username):
    user = CustomUser.objects.get(username=username)
    posts = Post.objects.filter(author=user).order_by('-created_at')
    follower_count = user.followers.count()
    is_following = user.followers.filter(follower=request.user).exists()
    
    update_profile_form = UserProfileForm(instance=user)

    if request.method == 'POST':
        update_profile_form = UserProfileForm(request.POST, request.FILES, instance=user)
        if update_profile_form.is_valid():
            update_profile_form.save()
            return redirect('user-detail', username=username)

    context = {
            'user': user,
            'follower_count': follower_count,
            'is_following': is_following,
            'posts' : posts,
            'update_profile_form': update_profile_form
    }
    
    return render(request, 'ui_service/user_profile.html', context)

def chat_page(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    chats = Chat.objects.filter(sender=request.user, receiver=user) | Chat.objects.filter(sender=user, receiver=request.user)
    return render(request, 'ui_service/chat.html', {'user': user, 'chats': chats})

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
    

class CommentDetailView(View):
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        text = comment.text
        return JsonResponse({'text': text})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
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
        existing_file_name = post.media_url.split('/')[-1]
        blob = storage.bucket(BUCKET_NAME).blob('post_media/' + str(post.id) + '/' + existing_file_name)
        blob.delete()

    bucket = storage.bucket(BUCKET_NAME)
    blob = bucket.blob('post_media/' + str(post.id) + '/' + file.name)
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
            print("AnhWasHere")
            print(post.id)

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

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            post = form.save(commit=False)
            post.save()
            if 'media' in request.FILES:
                media_file = request.FILES['media']
                try:
                    update_media(post, media_file)
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
            return redirect('post-detail', pk=pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'ui_service/edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user == post.author or request.user.is_superuser:
        if request.method == 'POST':
            post.delete()
            return redirect('home')

        return render(request, 'ui_service/delete_post.html', {'post': post})

    return HttpResponseForbidden()

@login_required
def share_post(request, post_id):
    post = Post.objects.get(pk=post_id)

    post.share_count += 1
    post.save()

    return JsonResponse({'share_count': post.share_count})

@login_required
def get_comments(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post).order_by('created_at')
    
    comments_data = []
    for comment in comments:
        comments_data.append({
            'id': comment.id,
            'text': comment.text,
            'like_count': comment.like_count, 
            'user' : comment.user.username,
            'avatar_url' : comment.user.avatar_url,
            'created_at' : comment.created_at,
            'is_authenticated': request.user.is_authenticated,
            'is_comment_author': comment.user.username == request.user.username,
        })

    return JsonResponse(comments_data, safe=False)

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
            post.comment_count += 1
            post.save()

            comment_data = {
                'id': comment.id,
                'text': comment.text,
                'user': comment.user.username,
                'avatar_url': comment.user.avatar_url,
                'created_at': comment.created_at.isoformat(),
                'post_id': comment.post.id,
                'like_count' : comment.like_count,
            }
            
            return JsonResponse(comment_data)
        
        print(comment_form.errors.as_json())

    return JsonResponse({'error': 'Invalid form data'}, status=400)


@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.user != comment.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            
            # Reload the comment to get the updated content
            updated_comment = Comment.objects.get(pk=comment.pk)
            
            # Return JSON response with the updated comment data
            comment_data = {
                'id': updated_comment.id,
                'text': updated_comment.text,
                'user': updated_comment.user.username,
                'avatar_url': updated_comment.user.avatar_url,
                'created_at': updated_comment.created_at.isoformat(),
                'post_id': updated_comment.post.id,
                'like_count' : updated_comment.like_count,
            }

            return JsonResponse({'success': True, 'comment': comment_data})
        else:
            print(form.errors.as_json())  # Add this line to log form errors
    else:
        print('Invalid request method')  # Add this line to log invalid request method

    return JsonResponse({'success': False, 'error': 'Invalid form data'}, status=400)

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.user != comment.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        post_id = comment.post.id  # Get the post PK before deleting the comment
        comment.delete()

        # Update the comment count in the corresponding post
        post = get_object_or_404(Post, pk=post_id)
        post.comment_count = Comment.objects.filter(post=post).count()
        post.save()
        print(post)
        return JsonResponse({'success': True, 'post_id': post_id})

    return render(request, 'ui_service/delete_comment.html', {'comment': comment})
    
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
def follow_unfollow_user(request, username):
    user_to_follow = get_object_or_404(CustomUser, username=username)
    if user_to_follow == request.user:
        return redirect('user-profile', username=username)
    
    is_following = Follower.objects.filter(user=user_to_follow, follower=request.user).exists()
    if is_following:
        Follower.objects.filter(user=user_to_follow, follower=request.user).delete()
    else:
        Follower.objects.create(user=user_to_follow, follower=request.user)

    return redirect('user-profile', username=username)


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

@login_required
def update_profile(request, username):
    user = CustomUser.objects.get(username=username)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('user-detail', username=username)
    else:
        profile_form = UserProfileForm(instance=user)

    return render(request, 'ui_service/update_profile.html', {'profile_form': profile_form, 'user': user})


class ChatView(View):
    template_name = 'ui_service/chat.html'

    def get(self, request, recipient_id):
        # Pass recipient_id to the context to use in the template
        context = {'recipient_id': recipient_id}
        return render(request, self.template_name, context)

@login_required
def chat(request, user_id):
    receiver = CustomUser.objects.get(id=user_id)
    return render(request, 'ui_service/chat.html', {'receiver': receiver})

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
        posts = Post.objects.all().order_by('-created_at')

        return render(request, 'ui_service/home.html', {'form': form, 'posts': posts})
        
    return render(request, 'ui_service/home.html', {'form': form})