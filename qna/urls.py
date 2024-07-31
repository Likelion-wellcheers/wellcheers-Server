from django.urls import path

from qna.views import QnA, QuestionList

urlpatterns = [
    path("", QnA.as_view()),
    path("<int:region_id>/question/", QuestionList.as_view()),
]