from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('storeApp.urls')),
    path('customer/', include('customerApp.urls')),
    path('api/', include('api.urls')),
    path('theAdmin/', include('theAdmin.urls')),
]
