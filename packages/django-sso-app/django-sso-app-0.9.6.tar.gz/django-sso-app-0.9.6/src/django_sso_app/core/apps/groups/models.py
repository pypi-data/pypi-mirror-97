import logging

from django.contrib.auth.models import Group as DjangoGroup
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

logger = logging.getLogger('django_sso_app.core.apps.groups')


class Group(DjangoGroup):
    class Meta:
        proxy = True
        app_label = 'django_sso_app'
        verbose_name = _('Group')

    def get_relative_rest_url(self):
        return reverse("django_sso_app_group:rest-detail", args=[self.pk])
