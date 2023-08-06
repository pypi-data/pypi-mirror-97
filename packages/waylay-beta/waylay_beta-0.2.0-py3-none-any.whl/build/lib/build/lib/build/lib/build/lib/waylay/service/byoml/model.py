"""REST definitions for the 'model' entity of the 'byoml' service."""

from zipfile import ZipFile
from io import BytesIO
from functools import wraps
from typing import Callable, List, Any, Union, Tuple
import os
import joblib

import pandas as pd
import numpy as np

from .._base import WaylayResource
from .._decorators import (
    return_body_decorator,
    return_path_decorator,
    suppress_header_decorator
)
from ._decorators import (
    byoml_exception_decorator
)
from ...exceptions import (
    RestRequestError,
    ByomlValidationError,
)


def _input_data_as_list(input_data):
    if isinstance(input_data, list):
        return input_data
    if isinstance(input_data, pd.DataFrame):
        return input_data.values.tolist()
    # numpy nd_array
    try:
        return input_data.tolist()
    except (ValueError, TypeError):
        pass
    raise RestRequestError(
        f'input data of unsupported type {type(input_data)}'
    )


def model_execution_request_decorator(action_method):
    """Decorate an action to prepare the execution of the model.

    Transforms any input data into a list, and provides it
    as `instances` in the request body.
    """
    @wraps(action_method)
    def wrapped(model_name, input_data, **kwargs):
        request_body = {
            'instances': _input_data_as_list(input_data)
        }
        return action_method(
            model_name,
            body=request_body,
            **kwargs
        )
    return wrapped


DEFAULT_DECORATORS = [byoml_exception_decorator, return_body_decorator]


def _execute_model_decorators(response_key: str) -> List[Callable]:
    return [
        byoml_exception_decorator,
        model_execution_request_decorator,
        return_path_decorator(
            [response_key],
            default_response_constructor=np.array
        )
    ]


DEFAULT_BYOML_MODEL_TIMEOUT = 60


class ModelResource(WaylayResource):
    """REST Resource for the 'model' entity of the 'byoml' service."""

    link_roots = {
        'doc': '${doc_url}/api/byoml/',
        'iodoc': '${iodoc_url}/api/byoml/?id='
    }

    actions = {
        'list': {
            'method': 'GET',
            'url': '/models',
            'decorators': [
                byoml_exception_decorator,
                return_path_decorator(['available_models'])
            ],
            'description': 'List the metadata of the deployed <em>BYOML Models</em>',
            'links': {
                'doc': '#overview-of-the-api',
                'iodoc': 'overview-of-the-api'
            },
        },
        'list_names': {
            'method': 'GET',
            'url': '/models',
            'decorators': [
                byoml_exception_decorator,
                return_path_decorator(['available_models', 'name'])
            ],
            'description': 'List the names of deployed <em>BYOML Models</em>',
            'links': {
                'doc': '#overview-of-the-api',
                'iodoc': 'overview-of-the-api'
            },
        },
        '_create': {
            'method': 'POST',
            'url': '/models',
            'decorators': DEFAULT_DECORATORS,
            'description': (
                'Build and create a new <em>BYOML Model</em> as specified in the request'
            ),
            'name': 'create',
            'links': {
                'doc': '#how-to-upload-your-model',
                'iodoc': 'how-to-upload-your-model'
            },
        },
        '_replace': {
            'method': 'PUT',
            'url': '/models/{}',
            'name': 'replace',
            'decorators': DEFAULT_DECORATORS,
            'description': 'Build and replace the named <em>BYOML Model</em>',
            'links': {
                'doc': '#overwriting-a-model',
                'iodoc': 'overwriting-a-model'
            },
        },
        'get': {
            'method': 'GET',
            'url': '/models/{}',
            'decorators': DEFAULT_DECORATORS,
            'description': 'Fetch the metadata of the named <em>BYOML Model</em>',
            'links': {
                'doc': '#checking-out-your-model',
                'iodoc': 'checking-out-your-model'
            },
        },
        'get_content': {
            'method': 'GET',
            'url': '/models/{}/content',
            'decorators': [byoml_exception_decorator],
            'description': 'Fetch the content of the named <em>BYOML Model</em>',
            'links': {
                'doc': '#checking-out-your-model',
                'iodoc': 'checking-out-your-model'
            },
        },
        'examples': {
            'method': 'GET',
            'url': '/models/{}/examples',
            'decorators': [
                byoml_exception_decorator,
                return_path_decorator(['example_payloads'])
            ],
            'description': (
                'Fetch the <em>example request input</em> of the named <em>BYOML Model</em>'
            ),
            'links': {
                'doc': '#example-input',
                'iodoc': 'example-input'
            },
        },
        'predict': {
            'method': 'POST',
            'url': '/models/{}/predict',
            'decorators': _execute_model_decorators('predictions'),
            'description': (
                'Execute the <em>predict</em> capability of the named <em>BYOML Model</em>'
            ),
            'links': {
                'doc': '#predictions',
                'iodoc': 'predictions'
            },
        },
        'regress': {
            'method': 'POST',
            'url': '/models/{}/regress',
            'decorators': _execute_model_decorators('result'),
            'description': (
                'Execute the <em>regress</em> capability of the named  <em>BYOML Model</em>'
            ),
            'links': {
                'doc': '#predictions',
                'iodoc': 'predictions'
            },
        },
        'classify': {
            'method': 'POST',
            'url': '/models/{}/classify',
            'decorators': _execute_model_decorators('result'),
            'description': (
                'Execute the <em>classification</em> capability of the named <em>BYOML Model</em>'
            ),
            'links': {
                'doc': '#predictions',
                'iodoc': 'predictions'
            },
        },
        'remove': {
            'method': 'DELETE',
            'url': '/models/{}',
            'decorators': DEFAULT_DECORATORS,
            'description': 'Remove the named <em>BYOML Model</em>',
            'links': {
                'doc': '#deleting-a-model',
                'iodoc': 'deleting-a-model'
            },
        },
    }

    def __init__(self, *args, **kwargs):
        """Create a ModelResource."""
        kwargs.pop('timeout', None)
        super().__init__(*args, timeout=DEFAULT_BYOML_MODEL_TIMEOUT, **kwargs)

    def _get_files_to_zip(self, file_or_dir: str) -> List[Tuple[str, str]]:
        """Get the filenames to zip and the name it should have in the zipfile."""
        if not os.path.isdir(file_or_dir):
            # single file
            zip_file_name = os.path.basename(file_or_dir)
            return [(file_or_dir, zip_file_name)]

        file_names: List[Tuple[str, str]] = []
        for root, _, files in os.walk(file_or_dir):
            for file_name in files:
                # the root will always contain the same suffix, which should not end up in the zip
                zip_root = root[len(file_or_dir):]
                zip_file_name = os.path.join(zip_root, file_name)

                file_path = os.path.join(root, file_name)

                file_names.append((file_path, zip_file_name))

        return file_names

    def _send_model_arguments(
        self, model_name: str, trained_model: Union[str, Any],
        framework: str = "sklearn", description: str = ""
    ):
        """Upload a binary model with given name, framework and description."""
        # be backwards compatible for sklearn models
        if not isinstance(trained_model, str):
            # this works only for sklearn models
            if framework != 'sklearn':
                raise ByomlValidationError(
                    'Passing the model is only supported for sklearn models, '
                    'provide the path to the saved model instead.'
                )

            file_name = './model.joblib'
            joblib.dump(trained_model, file_name)
            files = self._get_files_to_zip(file_name)
        else:
            files = self._get_files_to_zip(trained_model)

        model_zip_buffer = BytesIO()
        with ZipFile(model_zip_buffer, 'w') as zipper:
            for file_name, zip_file_name in files:
                zipper.write(file_name, zip_file_name)
        return {
            'body': {
                "name": model_name,
                "framework": framework,
                "description": description
            },
            'files': {
                "file": ('model.zip', model_zip_buffer.getvalue())
            },
        }

    @suppress_header_decorator('Content-Type')
    def upload(
        self,
        model_name: str,
        trained_model: Any,
        framework: str = "sklearn",
        description: str = "",
        **kwargs
    ):
        """Upload a new machine learning model with given name, framework and description.

        Parameters:
            model_name      the name of the model
            trained_model   the model object (will be serialised to an zip archive before upload)
            framework       one of the supported frameworks (default 'sklearn')
            description
            (other args)    passed onto the underlying 'POST /model/{name}' request
        """
        return self._create(  # pylint: disable=no-member
            **self._send_model_arguments(
                model_name, trained_model,
                framework=framework, description=description,
            ),
            **kwargs
        )

    @suppress_header_decorator('Content-Type')
    def replace(
        self,
        model_name: str,
        trained_model: Any,
        framework: str = "sklearn",
        description: str = "",
        **kwargs
    ):
        """Replace a machine learning model with given name, framework and description.

        Parameters:
            model_name      the name of the model
            trained_model   the model object (will be serialised to an zip archive before upload)
            framework       one of the supported frameworks (default 'sklearn')
            description
            (other)         passed onto the underlying 'PUT /model/{name}' request
        """
        return self._replace(   # pylint: disable=no-member
            model_name,
            **self._send_model_arguments(
                model_name, trained_model,
                framework=framework, description=description,
            ),
            **kwargs
        )
