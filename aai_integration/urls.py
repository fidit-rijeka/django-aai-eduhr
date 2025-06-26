from django.urls import include, path

from aai_integration.views import index

urlpatterns = [
    path('', index, name='index'),
    path('aai/', include('django_aai_eduhr.urls')),
]
