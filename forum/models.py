from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    pub_time = models.DateTimeField('Post Date', auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=3000)

    class Meta:
        ordering = ['-pub_time']


class Comment(models.Model):
    author = models.ForeignKey(User, related_name='p_comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='p_comments', on_delete=models.CASCADE)
    pub_time = models.DateTimeField('Comment Date', auto_now_add=True)
    text = models.TextField(max_length=400)

    def __str__(self):
        return self.text
