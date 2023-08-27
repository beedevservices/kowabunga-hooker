from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# All urls are at base /

urlpatterns = [
    path('', views.index),
    path('<int:id>/', views.catFilter),
    path('add/', views.addToCart),
    path('cart/', views.cart),
    path('logReg/', views.logReg),
    path('logout/', views.logout),
    path('thankyou/', views.thankYou),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)