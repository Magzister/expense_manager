from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings


from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view


schema_view = swagger_get_schema_view(
    openapi.Info(
        title='Expense manager API',
        default_version='1.0.0',
        description='API documentation for expense manager app'
    ),
    public=True
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('api/v1/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
