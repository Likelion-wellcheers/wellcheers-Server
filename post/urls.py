from django.urls import path
from .views import AtriclePost, ChoiceRegion, ArticlesByRegionView,MagazineByRegionView

urlpatterns = [
    path("region/", ChoiceRegion.as_view(), name='choiceregion.군구보여줌'),
    path("region/getarticle", ArticlesByRegionView.as_view(), name='region으로article리스트업'),
    path("region/getmagazine", MagazineByRegionView.as_view(), name="region으로magazine리스트업")
]