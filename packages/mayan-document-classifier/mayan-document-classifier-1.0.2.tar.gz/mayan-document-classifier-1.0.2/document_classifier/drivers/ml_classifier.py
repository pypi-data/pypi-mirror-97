import base64
import json
import logging
from typing import Dict

from google.cloud import aiplatform
from google.oauth2 import service_account
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.file_metadata.classes import FileMetadataDriver

from ..settings import setting_instances_arguments

__ALL__ = ('MachineLanguageClassifierDriver',)
logger = logging.getLogger(name=__name__)


class MachineLanguageClassifierDriver(FileMetadataDriver):
    label = _('ML classifier')
    internal_name = 'mlclassifier'

    def __init__(self, *args, **kwargs):
        self.read_settings()

    def _machine_language_image_classifier(
        self, credentials, file_object, instance_arguments
    ):
        instance_dict = {
            'content': base64.b64encode(file_object.read()).decode()
        }

        # The AI Platform services require regional API endpoints.
        client_options = {'api_endpoint': instance_arguments['api_endpoint']}

        # Initialize client that will be used to create and send requests.
        # This client only needs to be created once, and can be reused for
        # multiple requests.
        client = aiplatform.gapic.PredictionServiceClient(
            credentials=credentials,
            client_options=client_options
        )
        # The format of each instance should conform to the deployed model's
        # prediction input schema.
        instance = json_format.ParseDict(instance_dict, Value())
        instances = [instance]

        parameters_dict = {}
        parameters = json_format.ParseDict(parameters_dict, Value())

        endpoint = client.endpoint_path(
            project=instance_arguments['project'],
            location=instance_arguments['location'],
            endpoint=instance_arguments['endpoint']
        )

        response = client.predict(
            endpoint=endpoint, instances=instances, parameters=parameters
        )
        # The predictions are a google.protobuf.Value representation of the
        # model's predictions.
        result = []
        for prediction in response.predictions:
            result.append(dict(prediction))

        return result

    def _process(self, document_version):
        # Iterate over all the pages of the document passed.
        StoredCredential = apps.get_model(
            app_label='credentials', model_name='StoredCredential'
        )

        result = {}

        for instance_arguments in setting_instances_arguments.value:
            try:
                stored_credentials = StoredCredential.objects.get(
                    internal_name=instance_arguments['credentials_internal_name']
                )
            except TypeError:
                raise TypeError(
                    _(
                        'Setting "{}" must be a list.'.format(
                            setting_instances_arguments.global_name
                        )
                    )
                )

            stored_credentials_data = stored_credentials.get_backend_data()
            stored_credentials_data['type'] = 'service_account'

            credentials = service_account.Credentials.from_service_account_info(
                stored_credentials_data
            )

            for page_index, document_page in enumerate(document_version.pages.all()):
                cached_document_page_image_filename = document_page.generate_image()

                cache_file = document_page.cache_partition.get_file(
                    filename=cached_document_page_image_filename
                )

                with cache_file.open() as file_object:
                    """
                    The file_object provides the byte stream for the page, and
                    closes automatically when the context exits.
                    """
                    # Process document page image
                    result[page_index] = self._machine_language_image_classifier(
                        credentials=credentials, file_object=file_object,
                        instance_arguments=instance_arguments
                    )

        return result

    def read_settings(self):
        self.instances_arguments = setting_instances_arguments.value


# Associate the classifier to every MIME type
MachineLanguageClassifierDriver.register(mimetypes=('*',))
