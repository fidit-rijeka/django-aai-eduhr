from django.urls import include, path

urlpatterns = [
    path('', include('djangosaml2.urls')),
]
