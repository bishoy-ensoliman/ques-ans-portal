from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from django.utils import timezone
import datetime
from vote.models import VoteModel


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    country = CountryField(blank_label='select country...')
    phone_number = models.CharField(blank=True, default='', max_length=15)
    company = models.CharField(blank=True, default='', max_length=35)
    position = models.CharField(blank=True, default='', max_length=35)
    major_expr = models.CharField(blank=True, default='', max_length=35)
    profile_pic = models.ImageField(upload_to='accounts/profilepics/',
                                    default='default_avatar.png', blank=True)

    def __str__(self):  # __unicode__ for Python 2
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Question(models.Model):
    author = models.ForeignKey(User, related_name='questions', on_delete=models.CASCADE)
    pub_time = models.DateTimeField('Question Date', auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=3000)
    answered = models.BooleanField(default=False)

    class Meta:
        ordering = ['-pub_time']

    def __str__(self):
        return self.title

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_time <= now


class Answer(VoteModel, models.Model):
    author = models.ForeignKey(User, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    description = models.TextField(max_length=3000)
    pub_time = models.DateTimeField('Answer Date', auto_now_add=True)
    reviewed = models.BooleanField(default=False)

    def __str__(self):
        return '{}:{}'.format(self.author.get_full_name(), self.description)


class Step(models.Model):
    answer = models.ForeignKey(Answer, related_name='steps', on_delete=models.CASCADE)
    brief = models.CharField(max_length=400)
    in_detail = models.TextField(max_length=3000, blank=True)


class QuestionComment(models.Model):
    author = models.ForeignKey(User, related_name='q_comments', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='q_comments', on_delete=models.CASCADE)
    pub_time = models.DateTimeField('Comment Date', auto_now_add=True)
    text = models.TextField(max_length=400)

    def __str__(self):
        return self.text


class AnswerComment(models.Model):
    author = models.ForeignKey(User, related_name='a_comments', on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, related_name='a_comments', on_delete=models.CASCADE)
    pub_time = models.DateTimeField('Comment Date', auto_now_add=True)
    text = models.TextField(max_length=400)

    def __str__(self):
        return self.text
