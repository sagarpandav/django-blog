from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post

from rest_framework.decorators import api_view
from django.http import JsonResponse
from blog.entity_layer import entity_operations

# posts = [
#     {
#         'auther': 'Sagar Pandav',
#         'title': 'First Post',
#         'content': 'Hey There, Welcome to my first blog post',
#         'date_posted': 'March 11, 2018'
#     },
#     {
#         'auther': 'John Wick',
#         'title': 'About Me',
#         'content': 'I am the guy who once killed 3 guys with just a pencil!',
#         'date_posted': 'March 16, 2018'
#     }
# ]


# Create your views here.

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(auther=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.auther = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.auther = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.auther:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.auther:
            return True
        return False

def about(request):
    context = {
        'title': 'About'
    }
    return render(request, 'blog/about.html', context)

@api_view(['POST'])    
def get_pagewise_result(request):
    try: 
        db_name = request.POST['company_name']
        collection_name = request.POST['collection_name']
        user_id = request.POST['user_id']
        page_index = int(request.POST['page_index'])
        role = request.POST['role']
        json_result = entity_operations.get_pagewise_invoices(user_id, page_index, role,db_name, collection_name)
        return JsonResponse(json_result, safe=False)
    except Exception as error:
        print("get_pagewise_result error",error)
        # LOGGER.exception(error)