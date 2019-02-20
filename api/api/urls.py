from django.contrib import admin
from django.urls import path, include

router = [
    path('api/', include('categories.endpoints')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router))
]
