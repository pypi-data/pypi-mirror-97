# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['google-stubs', 'google-stubs.ads.google_ads.v5.proto.enums']

package_data = \
{'': ['*'],
 'google-stubs': ['ads/*',
                  'ads/google_ads/*',
                  'ads/google_ads/interceptors/*',
                  'ads/google_ads/v4/*',
                  'ads/google_ads/v4/proto/*',
                  'ads/google_ads/v4/proto/common/*',
                  'ads/google_ads/v4/proto/enums/*',
                  'ads/google_ads/v4/proto/errors/*',
                  'ads/google_ads/v4/proto/resources/*',
                  'ads/google_ads/v4/proto/services/*',
                  'ads/google_ads/v4/services/*',
                  'ads/google_ads/v4/services/transports/*',
                  'ads/google_ads/v5/*',
                  'ads/google_ads/v5/proto/*',
                  'ads/google_ads/v5/proto/common/*',
                  'ads/google_ads/v5/proto/errors/*',
                  'ads/google_ads/v5/proto/resources/*',
                  'ads/google_ads/v5/proto/services/*',
                  'ads/google_ads/v5/services/*',
                  'ads/google_ads/v5/services/transports/*',
                  'ads/google_ads/v6/*',
                  'ads/google_ads/v6/proto/*',
                  'ads/google_ads/v6/proto/common/*',
                  'ads/google_ads/v6/proto/enums/*',
                  'ads/google_ads/v6/proto/errors/*',
                  'ads/google_ads/v6/proto/resources/*',
                  'ads/google_ads/v6/proto/services/*',
                  'ads/google_ads/v6/services/*',
                  'ads/google_ads/v6/services/transports/*']}

install_requires = \
['google-ads>=9.0.0,<10.0.0',
 'googleapis-common-protos-stubs>=1.2.1,<2.0.0',
 'grpc-stubs>=1.24.5,<2.0.0',
 'typing-extensions>=3.7.4.3,<4.0.0.0']

setup_kwargs = {
    'name': 'google-ads-stubs',
    'version': '6.0.1',
    'description': 'Type stubs for google-ads',
    'long_description': "# Type stubs for the Google Ads API Client Library for Python\n\n[![PyPI version](https://badge.fury.io/py/google-ads-stubs.svg)](https://badge.fury.io/py/google-ads-stubs)\n\nThis package provides type stubs for the [Google Ads API Client Library for Python](https://github.com/googleads/google-ads-python). \nIt's currently compatible with v.9.0.0 of this library. It allows you to type check usage of the library with e.g. [mypy](http://mypy-lang.org/) and will also improve autocomplete in many editors.\n\n**This is in no way affiliated with Google.**\n\nThe stubs for protobuf messages were created by [mypy-protobuf](https://github.com/dropbox/mypy-protobuf).\nThe rest were created either by hand or by self-made scripts, with the output of MyPy's `stubgen` as\na starting point.\n\nIf you find incorrect annotations, please create an issue. Contributions for fixes are also welcome.\n\n## Installation\n\n```\n$ pip install google-ads-stubs\n```\n\n## Caveats\n\nThere are some caveats. The primary one is that type inference does _not_ work for the `get_type` and `get_service`\nmethods of `Client`. The workaround is to explicitly state the type. For `get_type` you can also instantiate\nthe object directly.\n\n```python\n# Replace this:\ncampaign_operation = client.get_type('CampaignOperation')\n# With this:\nfrom google.ads.google_ads.v3.types import CampaignOperation\ncampaign_operation: CampaignOperation = client.get_type('CampaignOperation')\n# Or this:\nfrom google.ads.google_ads.v3.types import CampaignOperation\ncampaign_operation = CampaignOperation()\n\n# Replace this:\ngoogle_ads_service = client.get_service('GoogleAdsService')\n# With this:\nfrom google.ads.google_ads.v3.services import GoogleAdsServiceClient\ngoogle_ads_service: GoogleAdsServiceClient = client.get_service('GoogleAdsService')\n```\n\nWhile it is technically possible to type these methods using a combination of overloading and literal types,\nthis is not included in these stubs. The reason is that it requires about 10,000 overloads, which, while simple\nto generate, slows type checking to a crawl.\n\nThis package does not provide complete type annotations, although it should cover what's used by most developers.\nThe bare output from `stubgen` is used by the ransport classes. These may be typed in the future if there is a need for it.\n\nSome service methods allow you to pass in either a protobuf message or a dictionary for certain arguments.\nThere is no check that the dictionary conforms to the message structure, as this would require a `TypedDict` subclass\nfor each message.\n",
    'author': 'Henrik Bruåsdal',
    'author_email': 'henrik.bruasdal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/henribru/google-ads-stubs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
