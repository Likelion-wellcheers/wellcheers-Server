from django.urls import path
from .views import Recommend, RegionInformation, CenterReview, CenterList, CenterView, MyCart, MyReport

urlpatterns = [
    path("", Recommend.as_view(), name='recommend'),
    path("<int:id>", RegionInformation.as_view(), name="Region_information"),
    path("<int:id>/center", CenterList.as_view(), name="CenterList"),
    path("center/<int:id>", CenterView.as_view(), name="CenterView"),
    path("mycart/", MyCart.as_view(), name="cartView"),
    path("mycart/<int:id>",MyCart.as_view(), name="cartPut"),
    path("mycart/report/<int:id>",MyReport.as_view(), name="ReportView")
]