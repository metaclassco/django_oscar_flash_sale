from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from oscar.app import application

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('', application.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
