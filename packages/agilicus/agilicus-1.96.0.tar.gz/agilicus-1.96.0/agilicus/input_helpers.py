import csv
import sys

import click

from typing import Any, Dict

from . import context


def update_if_not_none(obj: dict, new_values: dict):
    for k, v in new_values.items():
        if v is not None:
            obj[k] = v


def update_if_present(object: dict, key, **kwargs):
    value = kwargs.get(key, None)
    if value is not None:
        object[key] = value


def pop_item_if_none(obj: dict):
    if not obj:
        return

    keys_to_pop = []
    for k, v in obj.items():
        if v is None:
            keys_to_pop.append(k)
    for k in keys_to_pop:
        obj.pop(k)


def build_updated_model(klass, model, new_values):
    model_dict = model.to_dict()
    update_if_not_none(model_dict, new_values)
    return klass(**model_dict)


def get_org_from_input_or_ctx(ctx, org_id=None, **kwargs):
    if org_id is None:
        token = context.get_token(ctx)
        org_id = context.get_org_id(ctx, token)

    # Treat an empty-string org id like None so that we can query all if necessary
    if org_id == "":
        org_id = None

    return org_id


def get_user_id_from_input_or_ctx(ctx, user_id=None, **kwargs):
    if user_id is None:
        token = context.get_token(ctx)
        user_id = context.get_user_id(ctx, token)

    # Treat an empty-string like None so that we can query all if necessary
    if user_id == "":
        user_id = None

    return user_id


def parse_csv_input(input_filename, parser):
    input_file = sys.stdin
    if input_filename != "-":
        input_file = open(input_filename, "r")

    results = list()
    with input_file:
        csv_input = csv.DictReader(input_file, delimiter=",", quotechar='"')

        for result_dict in csv_input:
            result = parser(result_dict)
            if result:
                results.append(result)

    return results


class SubObjectType(click.ParamType):
    """
    SubObjectType allows us to map an input value to a specific location in an object
    we're building up.
      `location` identifies the sub object to map to (e.g. metadata).
      `base_type` identifies the type we're wrapping (e.g. click.INT)
    use `get_object_by_location` to extract the k,v pairs for a specific location.
    """

    def __init__(self, location, base_type: click.ParamType):
        self.location = location
        self.base_type = base_type
        self.name = base_type.name
        self._value = None

    def convert(self, value, param, ctx):
        self._value = self.base_type(value, param, ctx)
        return self

    def value(self):
        return self._value


class SubObjectString(SubObjectType):
    def __init__(self, location):
        super().__init__(location, click.STRING)


class SubObjectInt(SubObjectType):
    def __init__(self, location):
        super().__init__(location, click.INT)


def get_objects_by_location(location, objects: Dict[str, Any]) -> Dict[str, Any]:
    result = {}
    for key, obj in objects.items():
        if not isinstance(obj, SubObjectType):
            continue
        if obj.location != location:
            continue

        val = obj.value()
        if val is None:
            continue

        result[key] = val

    return result
