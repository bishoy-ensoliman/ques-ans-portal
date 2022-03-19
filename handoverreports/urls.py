from django.urls import path
from . import views

app_name = 'handover'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('add', views.add_document, name='add'),
    path('download', views.download, name='download'),
]
