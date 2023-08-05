# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bergen',
 'bergen.auths',
 'bergen.auths.backend',
 'bergen.auths.implicit',
 'bergen.auths.implicit.widgets',
 'bergen.auths.legacy',
 'bergen.clients',
 'bergen.extenders',
 'bergen.extenders.contexts',
 'bergen.managers',
 'bergen.messages',
 'bergen.messages.exceptions',
 'bergen.peasent',
 'bergen.postmans',
 'bergen.queries',
 'bergen.queries.delayed',
 'bergen.registries',
 'bergen.types',
 'bergen.types.node',
 'bergen.types.node.ports',
 'bergen.types.node.ports.ins',
 'bergen.types.node.ports.outs',
 'bergen.types.node.widgets',
 'bergen.ui',
 'bergen.ui.widgets',
 'bergen.wards',
 'bergen.wards.graphql']

package_data = \
{'': ['*']}

install_requires = \
['aiostream>=0.4.1,<0.5.0',
 'docstring-parser>=0.7.3,<0.8.0',
 'gql[all]>=3.0.0a5,<4.0.0',
 'namegenerator>=1.0.6,<2.0.0',
 'nest-asyncio>=1.5.1,<2.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'requests-oauthlib>=1.3.0,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'tqdm>=4.56.1,<5.0.0',
 'websockets>=8.1,<9.0']

setup_kwargs = {
    'name': 'bergen',
    'version': '0.3.42',
    'description': 'A python client for the Arnheim Framework',
    'long_description': '# Bergen\n\n### Idea\n\nBergen is the API-Client for the Arnheim Framework\n\n \n### Prerequisites\n\nBergen only works with a running Arnheim Instance (in your network or locally for debugging).\n\n### Usage\n\nIn order to initialize the Client you need to connect it as a Valid Application with your Arnheim Instance\n\n```python\nclient = Bergen(host="p-tnagerl-lab1",\n    port=8000,\n  client_id="APPLICATION_ID_FROM_ARNHEIM", \n  client_secret="APPLICATION_SECRET_FROM_ARNHEIM",\n  name="karl",\n)\n```\n\nIn your following code you can simple query your data according to the Schema of the Datapoint\n\n```python\nfrom bergen.schema import Node\n\nnode = Node.objects.get(id=1)\nprint(node.name)\n\n```\n\n## Access Data from different Datapoints\n\nThe Arnheim Framework is able to provide data from different Data Endpoints through a commong GraphQL Interface\n. This allows you to access data from various different storage formats like Elements and Omero and interact without\nknowledge of their underlying api.\n\nEach Datapoint provides a typesafe schema. Arnheim Elements provides you with an implemtation of that schema.\n\n## Provide a Template for a Node\n\nDocumentation neccesary\n\n\n### Testing and Documentation\n\nSo far Bergen does only provide limitedunit-tests and is in desperate need of documentation,\nplease beware that you are using an Alpha-Version\n\n\n### Build with\n\n- [Arnheim](https://github.com/jhnnsrs/arnheim)\n- [Pydantic](https://github.com/jhnnsrs/arnheim)\n\n\n#### Features\n\n- Scss\n- [Domain-style](https://github.com/reactjs/redux/blob/master/docs/faq/CodeStructure.md) for code structure\n- Bundle Size analysis\n- Code splitting with [react-loadable](https://github.com/jamiebuilds/react-loadable)\n\n\n## Roadmap\n\nThis is considered pre-Alpha so pretty much everything is still on the roadmap\n\n\n## Deployment\n\nContact the Developer before you plan to deploy this App, it is NOT ready for public release\n\n## Versioning\n\nThere is not yet a working versioning profile in place, consider non-stable for every release \n\n## Authors\n\n* **Johannes Roos ** - *Initial work* - [jhnnsrs](https://github.com/jhnnsrs)\n\nSee also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.\n\n## License\n\nAttribution-NonCommercial 3.0 Unported (CC BY-NC 3.0) \n\n## Acknowledgments\n\n* EVERY single open-source project this library used (the list is too extensive so far)',
    'author': 'jhnnsrs',
    'author_email': 'jhnnsrs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jhnnsrs/bergen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
