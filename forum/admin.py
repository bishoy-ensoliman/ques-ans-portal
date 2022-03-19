from django.contrib import admin
from .models import Post, Comment


class PostCommentInline(admin.TabularInline):
    model = Comment
    extra = 1


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    #readonly_fields = ('author',)
    fieldsets = [
        (None, {'fields': ['title']}),
        ('Description', {'fields': ['description'], 'classes': ['collapse']}),
        ('Author', {'fields': ['author']}),
    ]
    list_display = ('title', 'pub_time',)
    inlines = [PostCommentInline]
    list_filter = ['pub_time']
    search_fields = ['title']


admin.site.register(Post, PostAdmin)
