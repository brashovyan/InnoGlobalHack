from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as doc_urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/", include("mainapp.urls")),
]

urlpatterns += doc_urls

# это нужно для отображения картинок
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)