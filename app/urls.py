from django.urls import path
from django.views.generic import TemplateView
from .views import (
    QuizView, QuizResult, Captcha
)


urlpatterns = [
    path('', TemplateView.as_view(template_name='app/home.html'), name='home'),
    path('quiz/', QuizView.as_view(), name='quiz'),
    path('quiz/result/', QuizResult.as_view(), name='quiz_result'),
    path('captcha/', Captcha.as_view(), name="captcha"),
]
