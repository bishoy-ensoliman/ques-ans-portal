from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from .models import Question, Answer
from django.contrib.auth.models import User
from . import forms
from django.db.models import Q


# Create your views here.
class IndexView(generic.ListView, ):
    template_name = 'questions/index.html'
    context_object_name = 'latest_question_list'
    paginate_by = 8

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
         published in the future).
        """
        if self.request.method == 'GET':
            query = self.request.GET.get('q')
            if query:
                return Question.objects.filter(Q(title__contains=query) | Q(description__contains=query))
        return Question.objects.all()


class DetailView(generic.DetailView):
    model = Question
    template_name = 'questions/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_time__lte=timezone.now())


@login_required(login_url='/accounts/login/')
def add_question(request):
    if request.method == 'POST':
        form = forms.QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = User.objects.get(username=request.user)
            question.pub_time = timezone.now()
            question.save()
            return redirect('questions:add_answer', question.pk)
    else:
        form = forms.QuestionForm()
    return render(request, 'questions/add_question.html', {'form': form})


@login_required(login_url='/accounts/login/')
def edit_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if not (question.author == User.objects.get(pk=request.user.pk)):
        return redirect('questions:index')
    if request.method == 'POST':
        form = forms.QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = User.objects.get(username=request.user)
            question.pub_time = timezone.now()
            question.save()
            return redirect('questions:add_answer', question.pk)
    else:
        form = forms.QuestionForm(instance=question)
    return render(request, 'questions/add_question.html', {'form': form})


def in_reviewer_group(user):
    if user:
        return user.groups.filter(name='reviewer').count() != 0
    return False


@login_required
@user_passes_test(in_reviewer_group, login_url='/')
def review_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    question.answered = True
    question.save()
    return redirect('questions:index')


@login_required
@user_passes_test(in_reviewer_group, login_url='/')
def review_answer(request, qpk, apk):
    get_object_or_404(Question, pk=qpk)
    answer = get_object_or_404(Answer, pk=apk)
    answer.reviewed = True
    answer.save()
    return redirect('questions:detail', qpk)


@login_required(login_url='/accounts/login')
def delete_answer(request, qpk, apk):
    get_object_or_404(Question, pk=qpk)
    answer = get_object_or_404(Answer, pk=apk)
    if request.user.pk == answer.author.pk or in_reviewer_group(request.user):
        answer.delete()
    return redirect('questions:detail', qpk)


@login_required(login_url='/accounts/login/')
def add_answer(request, pk):
    get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        answer_form = forms.AnswerForm(request.POST)
        if answer_form.is_valid():
            created_answer = answer_form.save(commit=False)
            created_answer.question = Question.objects.get(pk=pk)
            created_answer.author = User.objects.get(username=request.user)
            created_answer.pub_time = timezone.now()
            formset = forms.StepInlineFormset(request.POST, instance=created_answer)
            if formset.is_valid():
                created_answer.save()
                formset.save()
                return redirect('questions:detail', pk)
        else:
            formset = forms.StepInlineFormset()
            return render(request, 'questions/add_answer.html',
                          {'form': answer_form, 'formset': formset, })
    else:
        form = forms.AnswerForm()
        formset = forms.StepInlineFormset()
        return render(request, 'questions/add_answer.html',
                      {'form': form, 'formset': formset, })


@login_required(login_url='/accounts/login/')
def add_q_comment(request, pk):
    get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = forms.QuestionCommentForm(request.POST)
        if form.is_valid():
            qcomment = form.save(commit=False)
            qcomment.author = User.objects.get(username=request.user)
            qcomment.question = Question.objects.get(pk=pk)
            qcomment.pub_time = timezone.now()
            qcomment.save()
            return redirect('questions:detail', pk)

    return redirect('questions:detail', pk)


@login_required(login_url='/accounts/login/')
def add_a_comment(request, qpk, apk):
    get_object_or_404(Question, pk=qpk)
    get_object_or_404(Answer, pk=apk)
    if request.method == 'POST':
        form = forms.AnswerCommentForm(request.POST)
        if form.is_valid():
            acomment = form.save(commit=False)
            acomment.author = User.objects.get(username=request.user)
            acomment.pub_time = timezone.now()
            acomment.answer = Answer.objects.get(pk=apk)
            acomment.save()
            return redirect('questions:detail', qpk)

    return redirect('questions:detail', qpk)


@login_required(login_url='/accounts/login/')
def upvote(request, qpk, apk):
    get_object_or_404(Question, pk=qpk)
    get_object_or_404(Answer, pk=apk)
    answer = Answer.objects.get(pk=apk)
    if request.method == 'POST':
        if not answer.votes.exists(request.user.pk, action=0):  # 0 = UP
            if answer.votes.exists(request.user.pk, action=1):
                if not answer.votes.delete(request.user.pk):
                    return HttpResponse("Delete Error")
            else:
                if not answer.votes.up(request.user.pk):
                    return HttpResponse("UPVOTE ERROR")
        answer.save()

    return redirect('questions:detail', qpk)


@login_required(login_url='/accounts/login/')
def downvote(request, qpk, apk):
    get_object_or_404(Question, pk=qpk)
    get_object_or_404(Answer, pk=apk)
    answer = Answer.objects.get(pk=apk)
    if request.method == 'POST':
        if not answer.votes.exists(request.user.pk, action=1):  # 1 = DOWN
            if answer.votes.exists(request.user.pk, action=0):
                if not answer.votes.delete(request.user.pk):
                    return HttpResponse("Delete Error")
            else:
                if not answer.votes.down(request.user.pk):
                    return HttpResponse("DOWNVOTE Error")
        answer.save()

    return redirect('questions:detail', qpk)
