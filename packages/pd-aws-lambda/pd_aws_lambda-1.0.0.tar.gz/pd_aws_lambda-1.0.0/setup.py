# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pd_aws_lambda', 'pd_aws_lambda.handlers', 'pd_aws_lambda.scripts']

package_data = \
{'': ['*']}

install_requires = \
['apig-wsgi>=2.0.0']

extras_require = \
{'deploy': ['boto3>=1.0.0']}

entry_points = \
{'console_scripts': ['pd_build = pd_aws_lambda.scripts.pd_build:run',
                     'pd_build_and_deploy = '
                     'pd_aws_lambda.scripts.pd_build_and_deploy:run',
                     'pd_deploy = pd_aws_lambda.scripts.pd_deploy:run',
                     'pd_run = pd_aws_lambda.scripts.pd_run:run']}

setup_kwargs = {
    'name': 'pd-aws-lambda',
    'version': '1.0.0',
    'description': '',
    'long_description': '===================================\nPython Deploy AWS Lambda Dispatcher\n===================================\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n\nHandle AWS Lambda events.\n\nEvents are passed to handlers for processing.\nEach event is passed to the handler in this order:\n\n- Handler defined in the event\n- Http events handler (for WSGI applications)\n- SQS events handler (if configured)\n- Default handler (if configured)\n- Logger handler (if no default is defined)\n\nProvided Handlers\n-----------------\n\n- `pd_aws_lambda.handlers.wsgi.handler`: convert HttpAPI requests to WSGI environs.\n- `pd_aws_lambda.handlers.shell.handler`: Run shell commands.\n- `pd_aws_lambda.handlers.logger.handler`: log the received event and context.\n\nUsage\n-----\n\n1. Add `pd-aws-lambda` to your application dependencies.\n\n   .. code-block:: console\n\n    poetry add pd-aws-lambda\n\n2. Set the required environment variables according to your needs in your\n   `Python Deploy`_ application configuration.\n\n   .. code-block:: ini\n\n    # Python path to the WSGI application that will handle Http requests.\n    PD_WSGI_APPLICATION=my_django_project.wsgi.application\n\n    # Python path to the handler for SQS events.\n    PD_SQS_HANDLER=my_custom_handlers.sqs_handler\n\n    # Python path to the default fallback handler.\n    PD_DEFAULT_HANDLER=my_custom_handlers.default_handler\n\nCustom handlers\n---------------\n\nA handler is a python function that receives an `event` and a `context` and\ndoes something with them. It can return a value if it makes sense for the type\nof event. For example, HttpAPI handlers like the one we use to call your wsgi\napplication (`pd_aws_lambda.handlers.wsgi.handler`) should return a dictionary\ncompatible with the `AWS HttpAPI`_ to form an Http response.\n\n.. code-block:: python\n\n    def handler(event, context):\n        """\n        I handle AWS Lambda invocations.\n\n        I print the received event and context.\n        """\n        print("The event:", event)\n        print("The context:", context)\n\n----\n\nDeveloped to be used with `Python Deploy`_.\n\n\n.. _AWS HttpAPI: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html\n.. _Python Deploy: https://pythondeploy.co\n',
    'author': 'Federico Jaramillo Martínez',
    'author_email': 'federicojaramillom@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
