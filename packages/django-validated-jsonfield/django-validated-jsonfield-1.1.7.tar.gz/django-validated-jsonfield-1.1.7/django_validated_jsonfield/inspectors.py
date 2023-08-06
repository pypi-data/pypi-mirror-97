from drf_yasg.inspectors import JSONFieldInspector


class ValidatedJSONFieldInspector(JSONFieldInspector):

    def add_manual_fields(self, serializer_or_field, schema):
        """Set fields from the ``swagger_schem_fields`` attribute on the Meta class. This method is called
        only for serializers or fields that are converted into ``openapi.Schema`` objects.
        :param serializer_or_field: serializer or field instance
        :param openapi.Schema schema: the schema object to be modified in-place
        """

        coreapi_schema = getattr(serializer_or_field, 'coreapi_schema', {})
        if coreapi_schema:
            for attr, val in coreapi_schema.items():
                setattr(schema, attr, val)

        meta = getattr(serializer_or_field, 'Meta', None)
        swagger_schema_fields = getattr(meta, 'swagger_schema_fields', {})
        if swagger_schema_fields:
            for attr, val in swagger_schema_fields.items():
                setattr(schema, attr, val)
