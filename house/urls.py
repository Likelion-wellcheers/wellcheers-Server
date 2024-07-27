from django.urls import path
from .views import Recommend, RegionInformation, CenterReview, CenterList, CenterView

urlpatterns = [
    path("result/", Recommend.as_view(), name='recommend'),
    path("result/<int:id>", RegionInformation.as_view(), name="Region_information"),
    path("result/<int:id>/center", CenterList.as_view(), name="CenterList"),
    path("result/center/<int:id>", CenterView.as_view(), name="CenterView"),
]