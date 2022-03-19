from django.forms import ModelForm
from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ('author', 'pub_time',)
        fields = ('title', 'description')


class PostCommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ('author', 'pub_time', 'post')
