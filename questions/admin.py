from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# Register your models here.
from .models import Profile, Answer, Question, Step, QuestionComment, AnswerComment


class StepInline(admin.TabularInline):
    model = Step
    show_change_link = True
    extra = 1


class AnswerInline(admin.TabularInline):
    model = Answer
    show_change_link = True
    extra = 1


class QuestionCommentInline(admin.TabularInline):
    model = QuestionComment
    extra = 1


class AnswerCommentInline(admin.TabularInline):
    model = AnswerComment
    extra = 1


class AnswerAdmin(admin.ModelAdmin):
   # readonly_fields = ('question',)
    fieldsets = [
        ('Question', {'fields': ['question']}),
        ('Author', {'fields': ['author']}),
        ('Short Answer', {'fields': ['description']}),
        ('reviewed?', {'fields': ['reviewed']}),

    ]
    list_display = ('question', 'description', 'pub_time', 'author', 'reviewed',)
    inlines = [StepInline, AnswerCommentInline]
    list_filter = ['pub_time', 'reviewed']
    search_fields = ['description']


# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    #readonly_fields = ('author',)
    fieldsets = [
        (None, {'fields': ['title']}),
        ('Description', {'fields': ['description'], 'classes': ['collapse']}),
        ('Author', {'fields': ['author']}),
        ('answered', {'fields': ['answered']})
    ]
    list_display = ('title', 'pub_time',)
    inlines = [AnswerInline, QuestionCommentInline]
    list_filter = ['pub_time', 'answered']
    search_fields = ['title']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
