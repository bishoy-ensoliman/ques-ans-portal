from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class HandoverReport(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default='')
    serial_num = models.CharField(max_length=16)
    file = models.FileField(upload_to='handovereports/', )
    approved = models.BooleanField(default=False)
    pub_time = models.DateTimeField(' Publication Date', default=timezone.now, editable=False)
# Create your models here.
