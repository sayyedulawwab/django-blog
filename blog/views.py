from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import CommentForm
from .models import Comment, Post


def home(request):
    context = {
        'posts': Post.objects.all()

    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def post_detail(request,pk):
    template = 'blog/post_detail.html'
    post = get_object_or_404(Post,pk=pk)
    comments = Comment.objects.filter(post__id=post.pk)
    return render(request, template, {
        'post':post,
        'comments':comments,
        'comment_form':None,
        'new_comment':None,
    })


def comment_create(request,pk):
    template_name = 'blog/post_detail.html'
    post = get_object_or_404(Post,pk=pk)
    comments = Comment.objects.filter(post__id=post.pk)
    new_comment = None
    if request.method == 'POST':    
        comment_form = CommentForm(data=request.POST)
        comment_form.author = request.user
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author=request.user
            new_comment.save()
            return HttpResponseRedirect(request.path_info)

    else:
        comment_form=CommentForm()
         
    return render(request, template_name,  {
        'post':post,
        'comments':comments,
        'new_comment':new_comment,
        'comment_form':comment_form,
    })

def comment_update(request,pk1,pk2):
    template_name = 'blog/post_detail.html'
    comment = get_object_or_404(Comment, pk=pk2)
    post = get_object_or_404(Post,pk=pk1)
    comments = Comment.objects.filter(post__id=post.pk)
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect('post-detail',pk=pk1)
   
    return render(request, template_name,  {
        'post':post,
        'comments':comments,
        'new_comment':comment,
        'comment_form':form,
    })

def comment_delete(request,pk1,pk2):
    comment = Comment.objects.get(pk=pk2)
    comment.delete()
    return redirect('post-detail',pk=pk1)
