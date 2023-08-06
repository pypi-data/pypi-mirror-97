# django_validated_jsonfield

django_validated_jsonfield is an inplace replacement for django JSONField which is validated against a json_schema

- A json_schema can be added to the field description
- The json_schema is used to validate the jsonfield data during full_clean or during restframework validation
- The field is also documented on Swagger (via drf_yasg specific inspectors)
- Missing data in the json structure is initialized/filled to the schema's default values

# Usage

## import

Replace your JSONField import

```python
from django.db.models import JSONField` or `from django.contrib.postgres.fields import JSONField
```

by 

```python
from django_validated_jsonfield import ValidatedJSONField as JSONField
```

## models
```python
class MyModel(models.Model):
    _data_schema = {
        "type": "object",
        "properties": {
            "en": {"type": ["string", "null"], "default":"",   "example":"Name", "title":"Name"}
            "fr": {"type": ["string", "null"], "default":"",   "example":"Nom",  "title":"Nom"}
        },
        "default": {}, #note the top level default
        "additionalProperties": False,
    }

    data = JSONField(schema=_data_schema, editable=True)
```

## Rest Framework serializers

### As defined field:

replace
```python
from rest_framework.serializers import JSONField
```
by
```python
from django_validated_jsonfield import ValidatedJSONFieldSerializer as JSONField
```

The updated JSONField expect to receive a "schema" and "json_validator_cls" argument at initilization.

### In serializers.ModelSerializer:

Add the ValidatedJsonModelSerializerMixin to your ModelSerializer classes.

```python
from django_validated_jsonfield import ValidatedJsonModelSerializerMixin

class MyModelSerializer(ValidatedJsonModelSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = MyModel
        exclude = []
```


## Swagger documentation (drf_yasg)

add the following block to your django settings.py file

```python
from django_validated_jsonfield.yasg import DEFAULT_FIELD_INSPECTORS
SWAGGER_SETTINGS = {
    'DEFAULT_FIELD_INSPECTORS': DEFAULT_FIELD_INSPECTORS
}
```

you should see the json field of your model being documented in Swagger


# Additional remarks

## json schema default

if the default field is provided in the json schema, the data will be initialized to the default value (if missing).
The feature works well only parents of nested fields in the json schema have a default themselves (to list or dict)
--> Note the "top level default" in the example above.

