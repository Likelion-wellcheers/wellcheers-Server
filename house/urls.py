from django.urls import path
from .views import Recommend

urlpatterns = [
    path("result/", Recommend.as_view(), name='recommend'),
    path("result/<int:id>", Recommend.as_view(), name="recommend_information")
]