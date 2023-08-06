# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['outcome',
 'outcome.eventkit',
 'outcome.eventkit.data',
 'outcome.eventkit.formats',
 'outcome.eventkit.mime',
 'outcome.eventkit.protocol_bindings']

package_data = \
{'': ['*']}

install_requires = \
['lark-parser>=0.10.1,<0.12.0',
 'outcome-utils>=5.0.0,<6.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'pydantic>=1.7.2,<2.0.0',
 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'outcome-eventkit',
    'version': '0.3.2',
    'description': 'A toolkit for emitting and handling events, following the CloudEvent spec.',
    'long_description': "# eventkit-py\n![ci-badge](https://github.com/outcome-co/eventkit-py/workflows/Release/badge.svg?branch=v0.3.2) ![version-badge](https://img.shields.io/badge/version-0.3.2-brightgreen)\n\nA toolkit for emitting and handling events, following the CloudEvent spec.\n\n## Installation\n\n```sh\npoetry add outcome-eventkit\n```\n\n## Usage\n\nIt's a good idea to be familiar with the [CloudEvent v1.0 spec](https://github.com/cloudevents/spec/blob/v1.0/spec.md) before using this library.\n\nThe library implements the following (but is extensible):\n\n- [The Core Event object](https://github.com/cloudevents/spec/blob/v1.0/spec.md)\n- [A JSON formatter](https://github.com/cloudevents/spec/blob/v1.0/json-format.md)\n- [The HTTP Protocol Bindings (Structured and Binary)](https://github.com/cloudevents/spec/blob/v1.0/http-protocol-binding.md)\n\n### Event Example\n```py\nfrom outcome.eventkit import CloudEvent, CloudEventData\nfrom outcome.eventkit.formats.json import JSONCloudEventFormat\nfrom outcome.eventkit.protocol_bindings.http import StructuredHTTPBinding, BinaryHTTPBinding\n\nimport requests\n\n# Create a payload, specifying how it will be encoded\ndata = CloudEventData(\n    data_content_type='application/json',\n    data={\n        'hello': 'world'\n    }\n)\n\n# Create an event\nevent = CloudEvent(type='co.outcome.events.sample', source='example', data=data)\n\n# Create a JSON representation of the event\nserialised_event = JSONCloudEventFormat.encode(event)\n\n# Or...\n\n# Create a HTTP message with the event\nhttp_message = BinaryHTTPBinding.to_http(event)\n\n# Or...\n\n# Create a structured HTTP message with the event and a JSON formatter\nhttp_message = StructuredHTTPBinding.to_http(event, JSONCloudEventFormat)\n\n# Post the event somewhere...\nrequests.post('http://example.org', headers=http_message.headers, data=http_message.body)\n```\n\n### Dispatch Example\n```py\nfrom outcome.eventkit import dispatch, CloudEvent\n\n# You can register event handlers that will be called\n# when a corresponding event is dispatched\n\n# Explicitly\ndef my_event_handler(event: CloudEvent) -> None:\n    ...\n\n# Register a handler for an event type\ndispatch.register_handler('co.outcome.event', my_event_handler)\n\n\n# Or via a decorator\n@dispatch.handles_events('co.outcome.event', 'co.outcome.other-event')\ndef my_other_handler(event: CloudEvent) -> None:\n    ...\n\n\n# Then notify all registered handlers of an event\nev = CloudEvent(type='co.outcome.event', source='example')\ndispatch.dispatch(ev)\n```\n\nBy default, all handlers are stored in a single registry, but you can provide your own registry to the `register_handler`/`handles_events`/`dispatch` methods with the `registry` keyword argument.\n\n```py\nfrom outcome.eventkit import dispatch\nfrom collections import defaultdict\n\nmy_registry: dispatch.CloudEventHandlerRegistry = defaultdict(list)\n\n@dispatch.handles_events('co.outcome.event', registry=my_registry)\ndef my_handler(event: CloudEvent) -> None:\n    ...\n\nev = CloudEvent(type='co.outcome.event', source='example')\ndispatch.dispatch(ev, registry=my_registry)\n```\n\n## Development\n\nRemember to run `./pre-commit.sh` when you clone the repository.\n",
    'author': 'Outcome Engineering',
    'author_email': 'engineering@outcome.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/outcome-co/eventkit-py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.6,<3.9.0',
}


setup(**setup_kwargs)
