from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.apiBase),
    path('allCustomers/', views.apiAllCustomers),
    path('allProducts/', views.apiAllProducts),
    path('allOrders/', views.apiAllOrders),
    path('allOrders-allCustomers/', views.apiAllByCust),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)