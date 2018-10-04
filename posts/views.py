"""Posts views."""

# Django
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView

# Forms
from posts.forms import PostForm

# Models
from posts.models import Post, Like

from django.shortcuts import redirect


class PostsFeedView(LoginRequiredMixin, ListView):
    """Return all published posts."""

    template_name = 'posts/feed.html'
    model = Post
    ordering = ('-created',)
    paginate_by = 30
    context_object_name = 'posts'


class PostDetailView(LoginRequiredMixin, DetailView):
    """Return post detail."""

    template_name = 'posts/detail.html'
    queryset = Post.objects.all()
    context_object_name = 'post'


class CreatePostView(LoginRequiredMixin, CreateView):
    """Create a new post."""

    template_name = 'posts/new.html'
    form_class = PostForm
    success_url = reverse_lazy('posts:feed')

    def get_context_data(self, **kwargs):
        """Add user and profile to context."""
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['profile'] = self.request.user.profile
        return context
    
 def toggle_like(request, pk):
    user = request.user
    post = Post.objects.get(pk=pk)
    like = Like.objects.filter(user=user).filter(post=post)
    response_data = {}
    if like:
        response_data['code'] = 204
        like.delete()
    else:
        response_data['code'] = 200
        Like.objects.create(user=user,post=post)
    response_data['message'] = 'success'
    return redirect('/')
