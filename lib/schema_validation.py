import os
from json import loads
from jsonschema import validate as schema_validate, RefResolver
import pkg_resources


def load_schema(schema_name):
    file_name = 'schemas/{name}.json'.format(name=schema_name)
    json_string = pkg_resources.resource_string('resources', file_name)
    return loads(json_string)


def validate(model_name, instance):
    base_url = os.path.abspath('resources') + '/schemas/'
    resolver = RefResolver(
        'file://{base_url}'.format(base_url=base_url),
        None)
    schema = load_schema(model_name)
    schema_validate(instance=instance, schema=schema, resolver=resolver)
