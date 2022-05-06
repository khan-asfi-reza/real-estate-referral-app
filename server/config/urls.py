from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

from . import settings


urlpatterns = [
                  path('admin/', admin.site.urls),
                  path("api/core/", include("server.apps.Core.urls")),
                  path("api/auth/", include("server.apps.Account.urls")),
                  path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
                  path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='swagger-ui'),
                  path('referral/', TemplateView.as_view(template_name="index.html"))
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
