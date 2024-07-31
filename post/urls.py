from django.urls import path
from .views import AtriclePost, ChoiceRegion, WellfareByRegionView,MagazineByRegionView

urlpatterns = [
    path("region/", ChoiceRegion.as_view(), name='choiceregion.군구보여줌'),
    path("region/getmagazine", MagazineByRegionView.as_view(), name='region으로매거진리스트업'),
    path("region/welfare", WellfareByRegionView.as_view(), name="region으로 복지정책 리스트업"),
    path("region/")
]