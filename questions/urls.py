from django.urls import path
from . import views

app_name = 'questions'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('add/', views.add_question, name='add_question'),
    path('<int:pk>/add_answer/', views.add_answer, name='add_answer'),
    path('<int:pk>/add_comment', views.add_q_comment, name='qcomment'),
    path('<int:qpk>/<int:apk>/add_comment', views.add_a_comment, name='acomment'),
    path('<int:qpk>/<int:apk>/upvote', views.upvote, name='upvote'),
    path('<int:qpk>/<int:apk>/downvote', views.downvote, name='downvote'),
    path('<int:pk>/edit', views.edit_question, name='edit'),
    path('<int:qpk>/<int:apk>/delete', views.delete_answer, name='delete'),
    path('<int:qpk>/<int:apk>/review', views.review_answer, name='review'),
    path('<int:pk>/review', views.review_question, name='q_review')
]
