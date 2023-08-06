# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_validated_jsonfield']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2.0',
 'djangorestframework>=3.11.0',
 'drf_yasg',
 'jsonschema',
 'jsonschema-to-openapi>=0.2.1',
 'py-openapi-schema-to-json-schema>=0.0.3,<0.0.4']

setup_kwargs = {
    'name': 'django-validated-jsonfield',
    'version': '1.1.9',
    'description': 'Add a schema with validation to your jsonfield',
    'long_description': '# django_validated_jsonfield\n\ndjango_validated_jsonfield is an inplace replacement for django JSONField which is validated against a json_schema\n\n- A json_schema can be added to the field description\n- The json_schema is used to validate the jsonfield data during full_clean or during restframework validation\n- The field is also documented on Swagger (via drf_yasg specific inspectors)\n- Missing data in the json structure is initialized/filled to the schema\'s default values\n\n# Usage\n\n## import\n\nReplace your JSONField import\n\n```python\nfrom django.db.models import JSONField` or `from django.contrib.postgres.fields import JSONField\n```\n\nby \n\n```python\nfrom django_validated_jsonfield import ValidatedJSONField as JSONField\n```\n\n## models\n```python\nclass MyModel(models.Model):\n    _data_schema = {\n        "type": "object",\n        "properties": {\n            "en": {"type": ["string", "null"], "default":"",   "example":"Name", "title":"Name"}\n            "fr": {"type": ["string", "null"], "default":"",   "example":"Nom",  "title":"Nom"}\n        },\n        "default": {}, #note the top level default\n        "additionalProperties": False,\n    }\n\n    data = JSONField(schema=_data_schema, editable=True)\n```\n\n## Rest Framework serializers\n\n### As defined field:\n\nreplace\n```python\nfrom rest_framework.serializers import JSONField\n```\nby\n```python\nfrom django_validated_jsonfield import ValidatedJSONFieldSerializer as JSONField\n```\n\nThe updated JSONField expect to receive a "schema" and "json_validator_cls" argument at initilization.\n\n### In serializers.ModelSerializer:\n\nAdd the ValidatedJsonModelSerializerMixin to your ModelSerializer classes.\n\n```python\nfrom django_validated_jsonfield import ValidatedJsonModelSerializerMixin\n\nclass MyModelSerializer(ValidatedJsonModelSerializerMixin, serializers.ModelSerializer):\n    class Meta:\n        model = MyModel\n        exclude = []\n```\n\n\n## Swagger documentation (drf_yasg)\n\nadd the following block to your django settings.py file\n\n```python\nfrom django_validated_jsonfield.yasg import DEFAULT_FIELD_INSPECTORS\nSWAGGER_SETTINGS = {\n    \'DEFAULT_FIELD_INSPECTORS\': DEFAULT_FIELD_INSPECTORS\n}\n```\n\nyou should see the json field of your model being documented in Swagger\n\n\n# Additional remarks\n\n## json schema default\n\nif the default field is provided in the json schema, the data will be initialized to the default value (if missing).\nThe feature works well only parents of nested fields in the json schema have a default themselves (to list or dict)\n--> Note the "top level default" in the example above.\n\n',
    'author': 'Loic Quertenmont',
    'author_email': 'loic@youmeal.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/loic.quertenmont/django_validated_jsonfield',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
