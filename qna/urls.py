from django.urls import path

from qna.views import QnA

urlpatterns = [
    path("", QnA.as_view()),
]