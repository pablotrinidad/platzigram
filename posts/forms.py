"""Post forms."""

# Django
from django import forms

# Models
from posts.models import Post, Comment


class PostForm(forms.ModelForm):
    """Post model form."""

    class Meta:
        """Form settings."""

        model = Post
        fields = ('user', 'profile', 'title', 'photo')


class CommentForm(forms.ModelForm):
    """Comment model form."""

    comment = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ("user", "profile", 'post', "comment")
