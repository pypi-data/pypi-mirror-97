JSON Schema Himarc
==================

Validate instance using `Himarc JSON schema <https://github.com/CIEPS/json-schema-himarc>`_
V1.0.3.

.. code-block:: python

    from json_schema_himarc import
        validate_himarc, get_himarc_validation_errors
    )
    instance = {}
    if not validate_himarc(instance):
        errors = get_himarc_validation_errors(instance)
