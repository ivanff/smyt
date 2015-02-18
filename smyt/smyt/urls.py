from django.conf.urls import patterns, include, url
from django.contrib import admin

from dynamic_models.views import index, DynamicModelSet, table_headers

urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^js_api/table/meta$', table_headers),
    url(r'^js_api/table/(?P<name>[-\w]+)/list$', DynamicModelSet.as_view({'get': 'list'})),
    url(r'^js_api/table/(?P<name>[-\w]+)$', DynamicModelSet.as_view({'post': 'create'})),
    url(r'^js_api/table/(?P<name>[-\w]+)/(?P<pk>\d+)$', DynamicModelSet.as_view({'put': 'update', 'delete': 'destroy'})),
    url(r'^admin/', include(admin.site.urls)),
)
