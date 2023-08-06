# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_lambda_powertools',
 'aws_lambda_powertools.logging',
 'aws_lambda_powertools.metrics',
 'aws_lambda_powertools.middleware_factory',
 'aws_lambda_powertools.shared',
 'aws_lambda_powertools.tracing',
 'aws_lambda_powertools.utilities',
 'aws_lambda_powertools.utilities.batch',
 'aws_lambda_powertools.utilities.data_classes',
 'aws_lambda_powertools.utilities.idempotency',
 'aws_lambda_powertools.utilities.idempotency.persistence',
 'aws_lambda_powertools.utilities.parameters',
 'aws_lambda_powertools.utilities.parser',
 'aws_lambda_powertools.utilities.parser.envelopes',
 'aws_lambda_powertools.utilities.parser.models',
 'aws_lambda_powertools.utilities.typing',
 'aws_lambda_powertools.utilities.validation']

package_data = \
{'': ['*']}

install_requires = \
['aws-xray-sdk>=2.5.0,<3.0.0',
 'boto3>=1.12,<2.0',
 'fastjsonschema>=2.14.5,<3.0.0',
 'jmespath>=0.10.0,<0.11.0']

extras_require = \
{'pydantic': ['pydantic>=1.6.0,<2.0.0', 'email-validator'],
 'pydantic:python_version < "3.8"': ['typing_extensions>=3.7.4.2,<4.0.0.0']}

setup_kwargs = {
    'name': 'aws-lambda-powertools',
    'version': '1.11.0',
    'description': 'Python utilities for AWS Lambda functions including but not limited to tracing, logging and custom metric',
    'long_description': "# AWS Lambda Powertools (Python)\n\n![Build](https://github.com/awslabs/aws-lambda-powertools/workflows/Powertools%20Python/badge.svg?branch=master)\n![PythonSupport](https://img.shields.io/static/v1?label=python&message=3.6%20|%203.7|%203.8&color=blue?style=flat-square&logo=python) ![PyPI version](https://badge.fury.io/py/aws-lambda-powertools.svg) ![PyPi monthly downloads](https://img.shields.io/pypi/dm/aws-lambda-powertools)\n\nA suite of Python utilities for AWS Lambda functions to ease adopting best practices such as tracing, structured logging, custom metrics, and more. ([AWS Lambda Powertools Java](https://github.com/awslabs/aws-lambda-powertools-java) is also available).\n\n**[📜Documentation](https://awslabs.github.io/aws-lambda-powertools-python/)** | **[API Docs](https://awslabs.github.io/aws-lambda-powertools-python/api/)** | **[🐍PyPi](https://pypi.org/project/aws-lambda-powertools/)** | **[Feature request](https://github.com/awslabs/aws-lambda-powertools-python/issues/new?assignees=&labels=feature-request%2C+triage&template=feature_request.md&title=)** | **[🐛Bug Report](https://github.com/awslabs/aws-lambda-powertools-python/issues/new?assignees=&labels=bug%2C+triage&template=bug_report.md&title=)** | **[Hello world example](https://github.com/aws-samples/cookiecutter-aws-sam-python)** | **[Detailed blog post](https://aws.amazon.com/blogs/opensource/simplifying-serverless-best-practices-with-lambda-powertools/)**\n\n> **Join us on the AWS Developers Slack at `#lambda-powertools`** - **[Invite, if you don't have an account](https://join.slack.com/t/awsdevelopers/shared_invite/zt-gu30gquv-EhwIYq3kHhhysaZ2aIX7ew)**\n\n## Features\n\n* **[Tracing](https://awslabs.github.io/aws-lambda-powertools-python/core/tracer/)** - Decorators and utilities to trace Lambda function handlers, and both synchronous and asynchronous functions\n* **[Logging](https://awslabs.github.io/aws-lambda-powertools-python/core/logger/)** - Structured logging made easier, and decorator to enrich structured logging with key Lambda context details\n* **[Metrics](https://awslabs.github.io/aws-lambda-powertools-python/core/metrics/)** - Custom Metrics created asynchronously via CloudWatch Embedded Metric Format (EMF)\n* **[Bring your own middleware](https://awslabs.github.io/aws-lambda-powertools-python/utilities/middleware_factory/)** - Decorator factory to create your own middleware to run logic before, and after each Lambda invocation\n* **[Parameters utility](https://awslabs.github.io/aws-lambda-powertools-python/utilities/parameters/)** - Retrieve and cache parameter values from Parameter Store, Secrets Manager, or DynamoDB\n* **[Batch processing](https://awslabs.github.io/aws-lambda-powertools-python/utilities/batch)** - Handle partial failures for AWS SQS batch processing\n* **[Typing](https://awslabs.github.io/aws-lambda-powertools-python/utilities/typing)** - Static typing classes to speedup development in your IDE\n* **[Validation](https://awslabs.github.io/aws-lambda-powertools-python/utilities/validation)** - JSON Schema validator for inbound events and responses\n* **[Event source data classes](https://awslabs.github.io/aws-lambda-powertools-python/utilities/data_classes)** - Data classes describing the schema of common Lambda event triggers\n* **[Parser](https://awslabs.github.io/aws-lambda-powertools-python/utilities/parser)** - Data parsing and deep validation using Pydantic\n\n### Installation\n\nWith [pip](https://pip.pypa.io/en/latest/index.html) installed, run: ``pip install aws-lambda-powertools``\n\n## Examples\n\n* [Serverless Shopping cart](https://github.com/aws-samples/aws-serverless-shopping-cart)\n* [Serverless Airline](https://github.com/aws-samples/aws-serverless-airline-booking)\n* [Serverless E-commerce platform](https://github.com/aws-samples/aws-serverless-ecommerce-platform)\n\n## Credits\n\n* Structured logging initial implementation from [aws-lambda-logging](https://gitlab.com/hadrien/aws_lambda_logging)\n* Powertools idea [DAZN Powertools](https://github.com/getndazn/dazn-lambda-powertools/)\n* [Gatsby Apollo Theme for Docs](https://github.com/apollographql/gatsby-theme-apollo/tree/master/packages/gatsby-theme-apollo-docs)\n\n## License\n\nThis library is licensed under the MIT-0 License. See the LICENSE file.\n",
    'author': 'Amazon Web Services',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/awslabs/aws-lambda-powertools-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
