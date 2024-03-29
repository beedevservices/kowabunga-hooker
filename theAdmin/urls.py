from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# All urls are at /theAdmin

urlpatterns = [
    path('', views.theAdmin),
    path('checkUser/', views.checkSuperUser),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)