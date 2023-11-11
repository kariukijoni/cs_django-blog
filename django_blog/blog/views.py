from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name='posts'
    ordering=['-date_posted']
    paginate_by = 2


class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_posts.html"
    context_object_name='posts'
    ordering=['-date_posted']
    paginate_by = 2

    # get posts of a specific user
    def get_queryset(self):
        user =get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model=Post


class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    fields=['title','content']

    # assign a post a user
    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Post
    fields=['title','content']

    # assign a post a user
    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    
    # check user edits own post only
    def test_func(self):
        post=self.get_object()
        if self.request.user == post.author:
            return True
        return False
    

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Post
    # redirect to after successful deletion
    success_url='/'

    # check user edits own post only
    def test_func(self):
        post=self.get_object()
        if self.request.user == post.author:
            return True
        return False
    

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})