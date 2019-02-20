from django.urls import path

from .views import get, post

app_name = 'rest_categories'

urlpatterns = [
    path('get/', get, name='get'),
    path('post/', post, name='post'),
]
