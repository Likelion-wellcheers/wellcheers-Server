from django.urls import path
from .views import AtriclePost, ChoiceRegion, WellfareByRegionView,MagazineByRegionView, Regionreview, Regionreviewlook,WellOne,MagOne

urlpatterns = [
    path("region/", ChoiceRegion.as_view(), name='choiceregion.군구보여줌'),
    path("<int:id>/getmagazine/", MagazineByRegionView.as_view(), name='region으로매거진리스트업'),
    path("<int:id>/welfare/", WellfareByRegionView.as_view(), name="region으로 복지정책 리스트업"),
    path("welfare/<int:id>/",WellOne.as_view(), name="정책개별보기"),
    path("getmagazine/<int:id>/",MagOne.as_view(),name="매거진개별보기"),
    path("<int:id>/review/", Regionreview.as_view(), name="지역리뷰 작성 삭제 리스트업"),
    path("review/<int:id>/",Regionreviewlook.as_view(), name="지역리뷰 개별보기")
]