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
    path('confirm/', views.confirmOrder),
    path('generateInvoice/<int:user_id>/<int:order_id>/', views.generateInvoice, name='invoice'),
    path('saveInvoice/', views.saveInvoice),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)