from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('question/', views.question, name='q'),
    path('question/<int:quiz_id>/<int:question_id>', views.question, name='question'),
    #path('quiz_picker/', views.quiz_picker, name='quiz_picker'),
]