from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . import models
from . import forms
from django.utils import timezone
from django.utils.encoding import smart_str
from Driller import settings
from wsgiref.util import FileWrapper
import mimetypes
from django.http import HttpResponse
import os
from django.db.models import Q


class IndexView(generic.ListView):
    template_name = 'handoverreports/index.html'
    context_object_name = 'library_files'
    paginate_by = 25

    def get_queryset(self):
        if self.request.method == 'GET':
            query = self.request.GET.get('q')
            if query:
                return models.HandoverReport.objects.filter(Q(title__contains=query) | Q(serial_num__contains=query))
        return models.HandoverReport.objects.all()


@login_required(login_url='/accounts/login/')
def add_document(request):
    if request.method == 'POST':
        form = forms.HandoverReportForm(request.POST, request.FILES)
        if form.is_valid():
            doc_file = form.save(commit=False)
            doc_file.author = User.objects.get(username=request.user)
            doc_file.pub_time = timezone.now()
            doc_file.save()
            return redirect('handover:index')

    else:
        form = forms.HandoverReportForm()
    return render(request, 'handoverreports/add_document.html', {'form': form})


def download(request):
    if request.method == 'GET':
        if request.GET.get('file'):
            file_name = request.GET.get('file')
            file_path = settings.MEDIA_ROOT + '/' + file_name.replace('media/', '')
            file_wrapper = FileWrapper(open(file_path, 'rb'))
            file_mimetype = mimetypes.guess_type(file_path)
            response = HttpResponse(file_wrapper, content_type=file_mimetype)
            response['Content-Length'] = os.stat(file_path).st_size
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
            return response
        else:
            return redirect('handover:index')
    return redirect('handover:index')
