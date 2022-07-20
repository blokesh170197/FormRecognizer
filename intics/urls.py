from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_swagger.views import get_swagger_view

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_swagger_view(title='Jaseci API')

schema_view = get_schema_view(
    openapi.Info(
        title="INTICS API",
        default_version='v2',
        description="Welcome to the world of zuci",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

context_path = 'copro/'

urlpatterns = [
    re_path(r'^doc(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),

    path(context_path + 'admin/', admin.site.urls),
    path(context_path + 'api/', include("app.urls")),
]
