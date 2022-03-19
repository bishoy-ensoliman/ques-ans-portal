from .models import HandoverReport
from django.forms import ModelForm


class HandoverReportForm(ModelForm):
    class Meta:
        model = HandoverReport
        exclude = ('pub_time', 'author', 'approved')
