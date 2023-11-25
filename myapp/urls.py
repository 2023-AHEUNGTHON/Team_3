from django.urls import path
from myapp.views import home, survey, result

urlpatterns = [
    path('', home, name='home'),
    path('survey/', survey, name='survey'),
    path('result/<str:usermbti>', result, name='result'),
]