from django.forms import ModelForm, CharField, inlineformset_factory
from .models import Question, Answer, Step, QuestionComment, AnswerComment


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        exclude = ('author', 'pub_time', 'answered')
        fields = ('title', 'description')


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        exclude = ('author', 'pub_time', 'reviewed',)
        fields = ('description',)


class StepForm(ModelForm):
    class Meta:
        model = Step
        exclude = ('answer',)


StepInlineFormset = inlineformset_factory(Answer, Step, form=StepForm, extra=1)


class QuestionCommentForm(ModelForm):
    class Meta:
        model = QuestionComment
        exclude = ('author', 'pub_time', 'question')


class AnswerCommentForm(ModelForm):
    class Meta:
        model = AnswerComment
        exclude = ('author', 'pub_time', 'answer')
