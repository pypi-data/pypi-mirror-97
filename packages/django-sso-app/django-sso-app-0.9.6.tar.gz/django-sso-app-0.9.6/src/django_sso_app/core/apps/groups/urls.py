from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import GroupApiViewSet


urlpatterns = [
    url(r'^$', GroupApiViewSet.as_view({'get': 'list'}), name="rest-list"),
    url(r'^(?P<pk>\w+)/$', GroupApiViewSet.as_view({'get': 'retrieve'}), name="rest-detail"),
]

urlpatterns = (format_suffix_patterns(urlpatterns), 'django_sso_app_group')
