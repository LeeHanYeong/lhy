"""
lhy URL Configuration
"""
import re
from collections import OrderedDict

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.renderers import ReDocRenderer as BaseReDocRenderer, OpenAPIRenderer
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from . import views

admin.site.site_title = 'lhy'
admin.site.site_header = 'lhy 관리자 페이지'


class SchemaGenerator(OpenAPISchemaGenerator):
    PATTERN_ERASE_WORDS = re.compile('|'.join(
        ['list', 'create', 'read', 'update', 'partial_update', 'destroy']))

    def get_paths_object(self, paths: OrderedDict):
        # operation_id에서, PATTERN_ERASE_WORDS에 해당하는 단어를 지운 후 오름차순으로 정렬
        def path_sort_function(path_tuple):
            operation_id = path_tuple[1].operations[0][1]['operationId']
            operation_id = self.PATTERN_ERASE_WORDS.sub('', operation_id)
            return operation_id

        paths = OrderedDict(sorted(paths.items(), key=path_sort_function))
        return super().get_paths_object(paths)


BaseSchemaView = get_schema_view(
    openapi.Info(
        title='lhy API',
        default_version='v1',
        description='lhy API Documentation',
        contact=openapi.Contact(email='dev@lhy.kr'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=SchemaGenerator,
)


class ReDocRenderer(BaseReDocRenderer):
    template = 'docs/redoc.html'


class RedocSchemaView(BaseSchemaView):
    renderer_classes = (ReDocRenderer, OpenAPIRenderer)


urlpatterns = [
    path('doc/', RedocSchemaView.as_cached_view(cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('health/', views.HealthCheckView.as_view(), name='health-check'),
    path('', views.IndexView.as_view(), name='index'),
]
if settings.DEBUG:
    try:
        import debug_toolbar

        urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
    except ModuleNotFoundError:
        pass
