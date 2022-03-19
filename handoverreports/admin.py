from django.contrib import admin
from .models import HandoverReport


# Register your models here.

# Register your models here.
class HandoverReportAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title']}),
        ('Serial Number', {'fields': ['serial_num']}),
        ('Author', {'fields': ['author']}),
        ('approved?', {'fields': ['approved']}),
        ('File', {'fields': ['file']})

    ]
    list_display = ('title', 'serial_num', 'file', 'pub_time', 'author', 'approved',)
    list_filter = ['pub_time', 'approved']
    search_fields = ['title', 'file', 'serial_num']


admin.site.register(HandoverReport, HandoverReportAdmin)
