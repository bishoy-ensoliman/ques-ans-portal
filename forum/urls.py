from django.urls import path
from . import views

app_name = 'forum'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>', views.DetailView.as_view(), name='detail'),
    path('add', views.add_post, name='add_post'),
    path('<int:pk>/comment', views.add_p_comment, name='p_comment'),

]
