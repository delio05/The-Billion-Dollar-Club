from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    re_path(r'^sentenceAnalyze/$', views.get_sentence, name='get_sentence'), 
    re_path(r'^feedback/$', views.get_feedback, name='get_feedback'), 
]