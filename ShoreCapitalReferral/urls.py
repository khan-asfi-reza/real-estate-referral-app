from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/core/", include("Core.urls")),
    path("api/auth/", include("Account.urls"))
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
 + static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
