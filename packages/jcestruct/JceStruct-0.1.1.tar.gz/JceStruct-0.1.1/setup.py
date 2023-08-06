# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jce']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.1,<2.0.0']

setup_kwargs = {
    'name': 'jcestruct',
    'version': '0.1.1',
    'description': 'JCE Encode/Decode',
    'long_description': '# Jce Struct\n\nTencent JCE Encode/Decode with fully pydantic support\n\n## Installation\n\n```bash\npip install JceStruct\n```\n\nor install from source (using poetry)\n\n```bash\npoetry add git+https://github.com/yanyongyu/JceStruct.git\n```\n\nor clone and install\n\n```bash\ngit clone https://github.com/yanyongyu/JceStruct.git\ncd JceStruct\npoetry install\n```\n\n## Usage\n\n### Create Struct\n\nCreate your struct by inheriting `JceStruct` and define your fields with `JceField`\n\n```python\nfrom jce import types, JceStruct, JceField\n\n\nclass ExampleStruct(JceStruct):\n    field1: types.INT32 = JceField(jce_id=1)\n    field2: float = JceField(jce_id=2, jce_type=types.DOUBLE)  # define type in options\n    field3: types.LIST[OtherStruct] = JceField(jce_id=3)  # nested struct supported\n    extra_pydantic_field: str = "extra_pydantic_field"  # other field is optional\n```\n\n### Encode/Decode\n\n```python\n# simple encode decode\nraw: ExampleStruct = ExampleStruct.decode(bytes, extra_pydantic_field="extra")\nbytes = raw.encode()\n\n# decode list from example struct\nraw = OtherStruct.decode_list(bytes, jce_id=3, **extra)\n```\n\n### Custom Encoder/Decoder\n\nJust inherit JceEncoder/JceDecoder and add it to your struct configuration\n\n```python\nfrom jce import JceStruct, JceEncoder\n\n\nclass CustomEncoder(JceEncoder):\n    pass\n\n\nclass ExampleStruct(JceStruct):\n\n    class Config:\n        jce_encoder = CustomEncoder\n        # jce_decoder = CustomDecoder\n```\n\n### Custom types\n\nJust inherit JceType and implement abstruct methods\n\n```python\nfrom jce import types\n\n\nclass CustomType(types.JceType):\n    ...\n```\n\n### Change default types\n\nBy default, head bytes are treated like this:\n\n```python\n{\n    0: BYTE,\n    1: INT16,\n    2: INT32,\n    3: INT64,\n    4: FLOAT,\n    5: DOUBLE,\n    6: STRING1,\n    7: STRING4,\n    8: MAP,\n    9: LIST,\n    10: STRUCT_START,\n    11: STRUCT_END,\n    12: ZERO_TAG,\n    13: BYTES\n}\n```\n\nfield will be converted to the type defined in struct when validate.\n\nto change it:\n\n```python\nclass ExampleStruct(JceStruct):\n\n    class Config:\n        jce_default_type = {\n            # add all types here\n        }\n```\n',
    'author': 'yanyongyu',
    'author_email': 'yanyongyu_1@126.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yanyongyu/JceStruct',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
