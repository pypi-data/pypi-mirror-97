# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['airplane']

package_data = \
{'': ['*']}

install_requires = \
['backoff>=1.10.0,<2.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'airplanesdk',
    'version': '0.2.0',
    'description': 'A Python SDK for writing Airplane tasks',
    'long_description': '# Airplane Python SDK [![PyPI](https://img.shields.io/pypi/v/airplanesdk)](https://pypi.org/project/airplanesdk/) [![PyPI - License](https://img.shields.io/pypi/l/airplanesdk)](./LICENSE) [![Docs](https://img.shields.io/badge/Docs-Python%20SDK-blue)](https://docs.airplane.dev/reference/runtime-api-and-airplane-sdk/python-sdk)\n\nAn SDK for writing Airplane tasks in Python.\n\n## Usage\n\nFirst, install the SDK:\n\n```sh\npip install airplanesdk\n```\n\nNext, you can use the SDK to produce outputs which will be separated from your logs:\n\n```python\nimport airplane\n\nairplane.write_output("Show me what you got")\n\n# You can also separate outputs into groups by attaching names:\nairplane.write_named_output("saying", "Show me what you got")\nairplane.write_named_output("saying", "Welcome to the club, pal")\nairplane.write_named_output("name", "Summer")\n```\n\nThis SDK can be used to programmatically kick off tasks and fetch their output:\n\n```python\n# You can get a task\'s ID from the URL bar, f.e.\n# https://app.airplane.dev/tasks/1oMt2mZC1DjkOZXxHH8BV57xrmF\ntask_id = "..."\nresp = airplane.run(task_id, {\n  # Optionally provide parameters to your task, using the same name\n  # as when templating a parameter into your task\'s CLI args.\n  "DryRun": True,\n})\n\n# run() will return the run\'s status (Succeeded, Failed, Cancelled) and a\n# dict of outputs, by name.\n#\n# Default outputs are available as `resp["outputs"]["output"]`.\nprint(resp["outputs"])\n```\n\n## Contributing\n\n### Deployment\n\nTo deploy a new version of this SDK:\n\n1. Bump the version number in `pyproject.toml` and `airplane/__init__.py`\n2. Run the following to build and publish to PyPI:\n\n```sh\npoetry publish --build --username=airplane\n```\n',
    'author': 'Airplane',
    'author_email': 'support@airplane.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://airplane.dev',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
