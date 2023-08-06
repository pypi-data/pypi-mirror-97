from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import Namespace

namespace = Namespace(
    label=_('Document classifier'), name='document_classifier'
)

setting_instances_arguments = namespace.add_setting(
    default=[], help_text=_(
        'Arguments to pass to the instance. Use a list to allow passing '
        'different arguments to each instance. Example: '
        '[{"project": "<project id>", "endpoint": "<deployed endpoint ID>", '
        '"location": "us-central1", "api_endpoint": '
        '"us-central1-prediction-aiplatform.googleapis.com",'
        '"pages_range": "[0-]"}]'
    ), global_name='DOCUMENT_CLASSIFIER_INSTANCES_ARGUMENTS'
)
