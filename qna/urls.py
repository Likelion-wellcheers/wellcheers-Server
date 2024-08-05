from django.urls import path

from qna.views import AnswerList, QnA, QuestionDetail, MyQuestion, MyAnswer, QuestionList, QusetionListByRegion

urlpatterns = [
    path("", QnA.as_view()),
    path("question/", QuestionList.as_view()),
    path("question/<int:q_id>/", QuestionDetail.as_view()),
    path("question/<int:q_id>/answer/", AnswerList.as_view()),
    path("myquestion/", MyQuestion.as_view()),
    path("myanswer/", MyAnswer.as_view()),
    path("question/region/<int:city_code>/", QusetionListByRegion.as_view()),
]