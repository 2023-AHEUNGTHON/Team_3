from django.urls import path
from django.contrib import admin
from myapp.views import home, category_list, SurveyView, StoreRecommendationView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('categories/', category_list, name='category_list'),
    path('survey/', SurveyView.as_view(), name='survey'),
    path('recommend_store/', StoreRecommendationView.as_view(), name='recommend_store')
]