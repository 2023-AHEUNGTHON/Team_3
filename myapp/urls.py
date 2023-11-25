from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin
from myapp.views import home, survey, result
from django.conf import settings


app_name = 'myapp'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('survey/', survey, name='survey'),
    path('result/<str:usermbti>', result, name='result'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)