from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import *
from django.contrib.auth import get_user_model
from .forms import *
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .utils import ObjectMixin

 
User = get_user_model()

class FollowIndex(LoginRequiredMixin, View):
    login_url = '/auth/login/'

    def get(self, request):
        favorite_list = Follow.objects.select_related('author', 'user').filter(user = request.user)
        author_list = [favorite.author for favorite in favorite_list]
        post_list = Post.objects.filter(author__in = author_list).order_by("-pub_date")
        paginator = Paginator(post_list, 10)
        page_number = request.GET.get('page') 
        page = paginator.get_page(page_number) 
        return render(request, 'follow.html', {'page': page, 'paginator': paginator})

class ProfileFollow(LoginRequiredMixin, View):
    login_url = '/auth/login/'

    def get(self, request, username):
        if request.user.username == username:
            return HttpResponse('Вы не можете подписаться на самого себя!')
       
        author = User.objects.get(username = username)
        try:
            follow = Follow.objects.get(user = request.user, author = author)
        except:
            follow = None
        if follow: 
            return HttpResponse('Вы уже подписаны на данного автора!')

        new_follow = Follow.objects.create(user = request.user, author = author)
        return redirect(reverse('profile',  kwargs={'username': username}))

class ProfileUnfollow(LoginRequiredMixin, View):
    login_url = '/auth/login/'

    def get(self, request, username):
        author = User.objects.get(username = username)
        follow = Follow.objects.get(user = request.user, author = author)
        follow.delete()
        return redirect(reverse('profile',  kwargs={'username': username}))
    
def page_not_found(request, exception):
        return render(request, "misc/404.html", {"path": request.path}, status=404)

def server_error(request):
        return render(request, "misc/500.html", status=500)
        
class Index(ObjectMixin, View):
    model = Post
    template = 'index.html'
    pag_num = 10

class GroupPosts(ObjectMixin, View):
    model = Group
    template = 'group.html'
    pag_num = 10

class Profile(ObjectMixin, View):
    model = Post
    template = 'profile.html'
    pag_num = 5

class PostView(View):

    def get(self, request, username, post_id):
        profile = get_object_or_404(User, username=username)
        post = get_object_or_404(Post, id=post_id)
        posts_count = Post.objects.filter(author__username = username).count()
        form = CommentForm()
        comments = Comment.objects.select_related('author', 'post').filter(post = post)
        return render(request, "post.html", {'comments': comments, 'form': form, "profile": profile, "post": post, 'posts_count': posts_count})

def check_author(func):
    
    def added_value(request, *args, **kwargs):
        post_id = kwargs['post_id']
        username = kwargs['username']
        post = get_object_or_404(Post, id= post_id)
        if request.request.user != post.author:
            return redirect(reverse('post',  kwargs={'username': username, 'post_id': post_id}))
        
        return func(request, *args, **kwargs)
               
    return added_value

class PostEdit(View):

    @check_author
    def get(self, request, username, post_id):
        post = get_object_or_404(Post, id= post_id)
        form = PostForm(instance = post)
        return render(request, "edit_post.html", {"form": form,'username':username, 'post':post})
    
    @check_author
    def post(self, request, username, post_id):
        post = get_object_or_404(Post, id=post_id)
        form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
        if form.is_valid():
            form.save()
    
            return redirect(reverse('post',  kwargs={'username': username, 'post_id': post_id}))
        return render(request, "edit_post.html", {"form": form})


class NewPost(LoginRequiredMixin, View):
    login_url = '/auth/login/'

    def get(self, request):
        form = PostForm()
        return render(request, "new_post.html", {"form": form})

    def post(self, request):
        form = PostForm(request.POST or None, files=request.FILES or None)
        if form.is_valid():
            new= form.save(commit = False)
            new.author = request.user
            new.save()
            
            return redirect(reverse('index'))
        return render(request, "new_post.html", {"form": form})


class AddComment(LoginRequiredMixin, View):
    login_url = '/auth/login/'

    def post(self, request, username, post_id):
        post = get_object_or_404(Post, id = post_id)
        form = CommentForm(request.POST or None)
        if form.is_valid():
            new = form.save(commit = False)
            new.author = request.user
            new.post = post
            new.save()
            
            return redirect(reverse('post',  kwargs={'username': username, 'post_id': post_id}))

        posts_count = Post.objects.filter(author__username = username).count()
        comments = Comment.objects.select_related('author', 'post').filter(post = post)
        profile = get_object_or_404(User, username=username)
        return render(request, "post.html", {'comments': comments, 'form': form, "profile": profile, "post": post, 'posts_count': posts_count})
