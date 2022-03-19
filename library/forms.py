from .models import DocFile
from django.forms import ModelForm


class DocFileForm(ModelForm):
    class Meta:
        model = DocFile
        exclude = ('pub_time', 'author', 'approved')
