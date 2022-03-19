from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class DocFile(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default='')
    file = models.FileField(upload_to='library/', )
    approved = models.BooleanField(default=False)
    pub_time = models.DateTimeField(' Publication Date', default=timezone.now, editable=False)
