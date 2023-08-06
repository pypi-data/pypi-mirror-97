# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dhis2',
 'dhis2.code_list',
 'dhis2.code_list.models',
 'dhis2.core',
 'dhis2.core.metadata',
 'dhis2.core.metadata.models',
 'dhis2.e2b',
 'dhis2.e2b.models',
 'dhis2.facility_list',
 'dhis2.facility_list.models',
 'dhis2.generate',
 'dhis2.generate.models']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'click>=7.1.2,<8.0.0',
 'fhir.resources>=5.1.1,<6.0.0',
 'lxml>=4.6.1,<5.0.0',
 'pydantic>=1.7.2,<2.0.0',
 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['dhis2 = dhis2.__main__:main']}

setup_kwargs = {
    'name': 'dhis2',
    'version': '0.7.5',
    'description': 'Tool for working and integrating with dhis2 instances',
    'long_description': '# dhis2-python: integration client for dhis2\n\n[![Package version](https://badge.fury.io/py/dhis2.svg)](https://pypi.python.org/pypi/dhis2)\n\n**Requirements**: Python 3.8+\n\n## Quickstart\n\nInstall using `pip`:\n\n```shell\n$ pip install dhis2\n```\n\nThis will install the `dhis2` command in your local environment (installing into a virtual environment recommended).\n\nThe tool supports a pluggable architecture, but the core supports:\n\n* Inspecting dhis2 instances\n    * `dhis2 -i inventory.yml inspect host-id/group-id`\n* Extracting mCSD and SVCM compatible payload, and pushing those to a FHIR compliant server\n    * `dhis2 -i inventory.yml facility-list mcsd mcsd-config.yml`\n    * `dhis2 -i inventory.yml code-list svcm svcm-config.yml`\n* Extract ICD 11 (MMS) `LinearizationEntities` as DHIS2 Option Sets\n  * `dhis2 -i inventory.yml code-list icd11 <icd11-host> --root-id <X>`\n* Extract ICD 10 `ICD10Entities` as DHIS2 Option Sets\n  * `dhis2 -i inventory.yml code-list icd10 <icd10-host> --root-id <X>`\n  * Please be aware that the icd11 docker image does _not_ include the icd10 code lists, so you have to use the public instance which requires API keys\n* Extract Individual Case Safety Reports E2B (R2) XML from DHIS2 instances that have installed the WHO AEFI package\n \n(see description of formats below)\n\nAs of now, we do not support sending data to dhis2, only extraction is supported.\n\n## Formats\n\n### Inventory\n\nThe inventory is where you will store all your services, and various groupings you might find useful (most commands will only work on single sources/targets though, with the exception of the `inspect` command currently)\n\nThe basic format is as follows\n\n```yaml\nhosts:\n  playdev:\n    type: dhis2\n    baseUrl: https://play.dhis2.org/dev\n    username: admin\n    password: district\n  playdemo:\n    type: dhis2\n    baseUrl: https://play.dhis2.org/demo\n    auth:\n      default:\n        type: http-basic\n        username: admin\n        password: district\n  fhirdemo:\n    type: fhir\n    baseUrl: http://localhost:8080/baseR4\n  icd11local:\n    type: icd11\n    baseUrl: http://localhost:8888\n  icd11official:\n    type: icd11\n    baseUrl: https://id.who.int\n    headers:\n      Authorization: Bearer YOUR_TOKEN\n  icd10official:\n    type: icd10\n    baseUrl: https://id.who.int\n    headers:\n      Authorization: Bearer YOUR_TOKEN\ngroups:\n  dhis2:\n    - playdev\n    - playdemo\n```\n\nThe keys of the `hosts` and `groups` block will be used to identifiy targets when using the `dhis2` commands.\n\nPlease note that:\n\n* Currently only `http-basic` is supported for dhis2\n* For fhir no authentication is supported (coming soon)\n\n### mCSD / SVCM configuration\n\nBoth mCSD and SVCM currently has the exact same format so we will describe them together. You will need a source host, target host (or some other target) and a set of filters if desired.\n\nBasic format\n\n```yaml\nsource:\n  id: playdev\ntarget:\n  id: fhirdemo\n```\n\nThis configuration would simply take all org unit or option sets inside of dhis2 and push them to a fhir instance.\n\nIf you would want to store the result instead, you can use the `log://` target\n\n```yaml\nsource:\n  id: playdev\ntarget:\n  id: log://\n\n```\n\n(this is also the default if no target is given)\n\n### Individual Case Safety Reports E2B (R2) configuration\n\nExtract of E2B R2 compatible XML is now supported in the tool. To use it, you will need a connection to a dhis2 instance with the DHIS2 WHO AEFI program,\nand for now only individual tracked entities can be extracted (more flexible query mechanism is coming)\n\nBasic dhis2 config\n\n```\nhosts:\n  d2aefi:\n    type: dhis2\n    baseUrl: https://dhis2-instance.com\n    username: username\n    password: password\n```\n\nExample command for extracting E2B XML\n\n`dhis2 -i inventory.yml e2b d2aefi --tracked-entity some-te-uid`\n',
    'author': 'Morten Hansen',
    'author_email': 'morten@dhis2.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dhis2/dhis2-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
