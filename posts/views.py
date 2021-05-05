"""Posts views."""

# Django
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import DeleteView

# Forms
from posts.forms import PostForm, CommentForm

# Models
from posts.models import Post, Comment


class PostsFeedView(LoginRequiredMixin, ListView):
    """Return all published posts."""

    template_name = 'posts/feed.html'
    model = Post
    ordering = ('-created',)
    paginate_by = 30
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.all()
        context['form_comments'] = CommentForm()
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    """Return post detail."""

    template_name = 'posts/detail.html'
    queryset = Post.objects.all()
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.get_object()).all()
        context['form_comments'] = CommentForm()
        return context



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


@login_required
def save_comment(request):
    """Save comments."""

    if request.method == 'POST':

        post = {
            "user": request.user.id,
            "profile": request.user.id,
            "comment": request.POST["comment"],
            "post": request.POST["post"]
        }

        form = CommentForm(post)

        if form.is_valid():
            form.save()
            return redirect("posts:feed")
    else:
        return HttpResponse(status=405)
    return HttpResponse(status=500)


class DeletePostView(LoginRequiredMixin, DeleteView):
    """Delete a post."""

    template_name = "posts/delete.html"
    model = Post
    success_url = reverse_lazy("posts:feed")

    def get_object(self):
        obj = super().get_object()
        obj.delete()
