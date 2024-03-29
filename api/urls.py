from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.apiBase),
    path('allData/', views.apiAllData),
    path('allCustomers/', views.apiAllCustomers),
    path('oneCustomer/<int:user_id>/', views.apiOneCustomer),
    path('allProducts/', views.apiAllProducts),
    path('oneProduct/<int:prod_id>/', views.apiOneProduct),
    path('allOrderNumbers/', views.apiAllOrderNumbers),
    path('oneOrderNumber/<str:orderNum>/', views.apiOneOrderNumber),
    path('allOrderItems/', views.apiAllOrderItems),
    path('allInvoiceNumbers/', views.apiAllInvoiceNumbers),
    path('oneInvoiceNumber/<str:orderNum>/', views.apiOneInvoiceNumber),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)