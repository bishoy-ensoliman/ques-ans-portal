from django.urls import path, include
from . import views

app_name = 'contact'
urlpatterns = [
    path('', views.contact, name='contact-us'),
    path('download/',views.download,name='download-app'),
]
