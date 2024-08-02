from django.urls import path

from qna.views import QnA, QuestionDetail, MyQuestion, MyAnswer

urlpatterns = [
    path("", QnA.as_view()),
    # path("question/", QuestionList.as_view()),
    path("question/<int:q_id>/", QuestionDetail.as_view()),
    path("myquestion/", MyQuestion.as_view()),
    path("myanswer/", MyAnswer.as_view()),
]