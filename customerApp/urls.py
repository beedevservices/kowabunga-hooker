from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# All urls are at /customer

urlpatterns = [
    path('login/', views.login),
    path('reg/', views.reg),
    path('order/', views.placeOrder),
    path('profile/', views.profile),
    path('profile/edit/', views.updateProfile),
    path('myOrders/', views.myOrders),
    path('confirm/', views.confirmOrder),
    path('generateInvoice/<int:order_id>/', views.generateInvoice, name='invoice'),
    path('saveInvoice/', views.saveInvoice, name='saveInvoice'),
    path('invoice/<int:invoice_id>/', views.viewPdf, name='viewInvoice'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    # http://127.0.0.1:8000/media/invoices/2023-MRdQ-30-oURn-8
    # http://127.0.0.1:8000/media/invoices/2023-MRdQ-30-oURn-8.pdf