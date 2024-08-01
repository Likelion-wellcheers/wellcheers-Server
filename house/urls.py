from django.urls import path
from .views import Recommend, RegionInformation, CenterReviewView, CenterList, CenterView, MyCart, MyReport, ReportWrite

urlpatterns = [
    path("", Recommend.as_view(), name='recommend'),
    path("<int:id>", RegionInformation.as_view(), name="Region_information"),
    path("<int:id>/center", CenterList.as_view(), name="CenterList"),
    path("center/<int:id>", CenterView.as_view(), name="CenterView"),
    path("center/<int:id>/review/", CenterReviewView.as_view(), name="CenterReviewView"),
    path("mycart/", MyCart.as_view(), name="cartView"),
    path("mycart/<int:id>",MyCart.as_view(), name="cartPut"),
    path("mycart/<int:id>",MyReport.as_view(), name="ReportView"),
    path("mycart/report",ReportWrite.as_view(),name="ReportWrite")
]