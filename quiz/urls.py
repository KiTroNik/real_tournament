from django.urls import path
from .views import RandomQuestion, AllQuestions

app_name = 'quiz_api'
urlpatterns = [
    path('random/', RandomQuestion.as_view(), name='random_question'),
    path('all/', AllQuestions.as_view(), name='questions'),
]
