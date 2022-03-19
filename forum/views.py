from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from .models import Post, Comment
from django.contrib.auth.models import User
from . import forms
from django.db.models import Q


# Create your views here.

class IndexView(generic.ListView, ):
    template_name = 'forum/index.html'
    context_object_name = 'latest_posts_list'
    paginate_by = 8

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
         published in the future).
        """
        if self.request.method == 'GET':
            query = self.request.GET.get('q')
            if query:
                return Post.objects.filter(Q(title__contains=query) | Q(description__contains=query))
        return Post.objects.all()


class DetailView(generic.DetailView):
    model = Post
    template_name = 'forum/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Post.objects.filter(pub_time__lte=timezone.now())


@login_required(login_url='/accounts/login/')
def add_post(request):
    if request.method == 'POST':
        form = forms.PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = User.objects.get(username=request.user)
            post.pub_time = timezone.now()
            post.save()
            return redirect('forum:detail', post.pk)
    else:
        form = forms.PostForm()
    return render(request, 'forum/add_post.html', {'form': form})


@login_required(login_url='/accounts/login/')
def add_p_comment(request, pk):
    get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = forms.PostCommentForm(request.POST)
        if form.is_valid():
            pcomment = form.save(commit=False)
            pcomment.author = User.objects.get(username=request.user)
            pcomment.post = Post.objects.get(pk=pk)
            pcomment.pub_time = timezone.now()
            pcomment.save()
            return redirect('forum:detail', pk)

    return redirect('forum:detail', pk)
