from django.contrib import admin
from .models import DocFile


# Register your models here.
class DocFileAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title']}),
        ('Author', {'fields': ['author']}),
        ('approved?', {'fields': ['approved']}),
        ('File', {'fields': ['file']})

    ]
    list_display = ('title', 'file', 'pub_time', 'author', 'approved',)
    list_filter = ['pub_time', 'approved']
    search_fields = ['title', 'file']


admin.site.register(DocFile, DocFileAdmin)
