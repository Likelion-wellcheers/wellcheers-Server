from django.urls import path
from .views import Recommend, RegionInformation

urlpatterns = [
    path("result/", Recommend.as_view(), name='recommend'),
    path("result/<int:id>", RegionInformation.as_view(), name="Region_information")
]