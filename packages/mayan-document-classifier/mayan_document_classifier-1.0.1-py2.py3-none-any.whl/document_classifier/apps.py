from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig

from .drivers import *  # NOQA


class DocumentClassifierApp(MayanAppConfig):
    app_namespace = 'document_classifier'
    app_url = 'document_classifier'
    has_tests = True
    name = 'document_classifier'
    verbose_name = _('Document classifier')

    def ready(self):
        super().ready()
