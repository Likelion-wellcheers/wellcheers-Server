from django.urls import path

from qna.views import QnA, QuestionList, QuestionDetail

urlpatterns = [
    path("", QnA.as_view()),
    path("<int:region_id>/", QuestionList.as_view()),
    path("question/<int:q_id>/", QuestionDetail.as_view()),
]