# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['open_alchemy',
 'open_alchemy.build',
 'open_alchemy.column_factory',
 'open_alchemy.facades',
 'open_alchemy.facades.code_formatter',
 'open_alchemy.facades.jsonschema',
 'open_alchemy.facades.sqlalchemy',
 'open_alchemy.helpers',
 'open_alchemy.helpers.ext_prop',
 'open_alchemy.helpers.peek',
 'open_alchemy.models_file',
 'open_alchemy.models_file.artifacts',
 'open_alchemy.models_file.model',
 'open_alchemy.models_file.models',
 'open_alchemy.schemas',
 'open_alchemy.schemas.artifacts',
 'open_alchemy.schemas.artifacts.property_',
 'open_alchemy.schemas.helpers',
 'open_alchemy.schemas.validation',
 'open_alchemy.schemas.validation.helpers',
 'open_alchemy.schemas.validation.property_',
 'open_alchemy.schemas.validation.property_.relationship',
 'open_alchemy.table_args',
 'open_alchemy.utility_base',
 'open_alchemy.utility_base.from_dict',
 'open_alchemy.utility_base.to_dict']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2,<3',
 'SQLAlchemy>=1.0,<2.0',
 'jsonschema>=3,<4',
 'sqlalchemy-stubs>=0.3,<0.5']

extras_require = \
{':python_version < "3.8"': ['typing_extensions>=3.7.4,<4.0.0']}

entry_points = \
{'console_scripts': ['openalchemy = open_alchemy.cli:main']}

setup_kwargs = {
    'name': 'openalchemy',
    'version': '2.3.0',
    'description': 'Maps an OpenAPI schema to SQLAlchemy models.',
    'long_description': '# OpenAlchemy\n\n![Code Quality Status](https://github.com/jdkandersson/OpenAlchemy/workflows/Code%20quality%20checks/badge.svg)\n![Azure DevOps coverage](https://img.shields.io/azure-devops/coverage/anderssonpublic/anderssonpublic/1)\n[![Documentation Status](https://readthedocs.org/projects/openapi-sqlalchemy/badge/?version=latest)](https://openapi-sqlalchemy.readthedocs.io/en/latest/?badge=latest)\n![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/jdkandersson/OpenAlchemy)\n![Code Climate technical debt](https://img.shields.io/codeclimate/tech-debt/jdkandersson/OpenAlchemy)\n![LGTM Grade](https://img.shields.io/lgtm/grade/python/github/jdkandersson/OpenAlchemy)\n\nTranslates an OpenAPI schema to SQLAlchemy models.\n\nSupports OpenAPI 3.0 and 3.1.\n\nGet started with the online editor that will guide you through using your\nexisting OpenAPI specification to define your database schema and offers\ninstalling your models using `pip`:\n[Online Editor](https://editor.openalchemy.io)\n\n## Installation\n\n```bash\npython -m pip install OpenAlchemy\n# To be able to load YAML file\npython -m pip install OpenAlchemy[yaml]\n```\n\n## Example\n\nFor example, given the following OpenAPI specification:\n\n```yaml\n# ./examples/simple/example-spec.yml\nopenapi: "3.0.0"\n\ninfo:\n  title: Test Schema\n  description: API to illustrate OpenAlchemy MVP.\n  version: "0.1"\n\npaths:\n  /employee:\n    get:\n      summary: Used to retrieve all employees.\n      responses:\n        200:\n          description: Return all employees from the database.\n          content:\n            application/json:\n              schema:\n                type: array\n                items:\n                  "$ref": "#/components/schemas/Employee"\n\ncomponents:\n  schemas:\n    Employee:\n      description: Person that works for a company.\n      type: object\n      x-tablename: employee\n      properties:\n        id:\n          type: integer\n          description: Unique identifier for the employee.\n          example: 0\n          x-primary-key: true\n          x-autoincrement: true\n        name:\n          type: string\n          description: The name of the employee.\n          example: David Andersson\n          x-index: true\n        division:\n          type: string\n          description: The part of the company the employee works in.\n          example: Engineering\n          x-index: true\n        salary:\n          type: number\n          description: The amount of money the employee is paid.\n          example: 1000000.00\n      required:\n        - id\n        - name\n        - division\n```\n\nThe SQLALchemy models file then becomes:\n\n```python\n# models.py\nfrom open_alchemy import init_yaml\n\ninit_yaml("./examples/simple/example-spec.yml")\n```\n\nThe _Base_ and _Employee_ objects can be accessed:\n\n```python\nfrom open_alchemy.models import Base\nfrom open_alchemy.models import Employee\n```\n\nWith the _models_filename_ parameter a file is auto generated with type hints\nfor the SQLAlchemy models at the specified location, for example:\n[type hinted models example](examples/simple/models_auto.py). This adds support\nfor IDE auto complete, for example for the model initialization:\n\n![autocomplete init](examples/simple/models_autocomplete_init.png)\n\nand for properties and methods available on an instance:\n\n![autocomplete instance](examples/simple/models_autocomplete_instance.png)\n\nAn extensive set of examples with a range of features is here:\n\n[examples for main features](examples)\n\nAn example API has been defined using connexion and Flask here:\n\n[example connexion app](examples/app)\n\n## Documentation\n\n[Read the Docs](https://openapi-sqlalchemy.readthedocs.io/en/latest/)\n\n## Buy me a coffee\n\n[![Buy Me A Coffee](https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png)](https://www.buymeacoffee.com/jdkandersson)\n\n## Features\n\n- initializing from JSON,\n- initializing from YAML,\n- build a package with the models for distribution, packaged as sdist or wheel,\n- automatically generate a models file,\n- `integer` (32 and 64 bit),\n- `number` (float only),\n- `boolean`,\n- `string`,\n- `password`,\n- `byte`,\n- `binary`,\n- `date`,\n- `date-time`,\n- generic JSON data,\n- `$ref` references for columns and models,\n- remote `$ref` to other files on the same file system\n  (_not supported on Windows_),\n- remote `$ref` to other files at a URL,\n- primary keys,\n- auto incrementing,\n- indexes,\n- composite indexes,\n- unique constraints,\n- composite unique constraints,\n- column nullability,\n- foreign keys,\n- default values for columns (both application and database side),\n- many to one relationships,\n- one to one relationships,\n- one to many relationships,\n- many to many relationships,\n- many to many relationships with custom association tables,\n- custom foreign keys for relationships,\n- back references for relationships,\n- `allOf` inheritance for columns and models,\n- joined and single table inheritance,\n- `from_str` model methods to construct from JSON string,\n- `from_dict` model methods to construct from dictionaries,\n- `to_str` model methods to convert instances to JSON string,\n- `__str__` model methods to support the python `str` function,\n- `__repr__` model methods to support the python `repr` function,\n- `to_dict` model methods to convert instances to dictionaries,\n- `readOnly` and `writeOnly` for influence the conversion to and from\n  dictionaries,\n- exposing created models under `open_alchemy.models` removing the need for\n  `models.py` files,\n- ability to mix in arbitrary classes into a model and\n- can use the short `x-` prefix or a namespaced `x-open-alchemy-` prefix for\n  extension properties.\n\n## Contributing\n\nFork and checkout the repository. To install:\n\n```bash\npoetry install\n```\n\nTo run tests:\n\n```bash\npoetry run pytest\n```\n\nMake your changes and raise a pull request.\n\n## Compiling Docs\n\n```bash\npoetry shell\ncd docs\nmake html\n```\n\nThis creates the `index.html` file in `docs/build/html/index.html`.\n\n## Release Commands\n\n```bash\nrm -r dist/*\npoetry build\npoetry publish\n```\n',
    'author': 'David Andersson',
    'author_email': 'anderssonpublic@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jdkandersson/OpenAlchemy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
