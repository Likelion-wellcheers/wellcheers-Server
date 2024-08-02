from django.urls import path
from .views import Home, CenterReviewLookView, Recommend, RegionInformation, CenterReviewView, CenterList, CenterView, MyCart, MyReport, MyCartInsert, ReportWrite

urlpatterns = [
    path("home/", Home.as_view(), name='home'),
    path("", Recommend.as_view(), name='recommend'),
    path("<int:id>/", RegionInformation.as_view(), name="Region_information"),
    path("<int:id>/center/", CenterList.as_view(), name="CenterList"),
    path("center/<int:id>/", CenterView.as_view(), name="CenterView"),
    path("center/<int:id>/review/", CenterReviewView.as_view(), name="CenterReviewView"),
    path("center/review/<int:id>/", CenterReviewLookView.as_view(), name="CenterReviewLookView"),
    path("mycart/", MyCartInsert.as_view(), name="cartView"),
    path("mycart/<int:id>/",MyCart.as_view(), name="cartPut"),
    path("mycart/<int:id>/budget/",MyReport.as_view(), name="ReportView"),
    path("mycart/report/",ReportWrite.as_view(),name="ReportWrite")
]