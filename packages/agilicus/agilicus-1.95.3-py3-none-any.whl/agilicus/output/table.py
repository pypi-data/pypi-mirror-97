import datetime
import operator

from agilicus import context
from agilicus.output.json import convert_to_json

from dataclasses import dataclass
from typing import Callable

from prettytable import PrettyTable


def format_date(date_input):
    return date_input.strftime("%Y-%m-%d %H:%M:%S %z (%Z)")


def date_else_identity(input_obj):
    if isinstance(input_obj, datetime.datetime):
        return format_date(input_obj)
    return input_obj


@dataclass
class OutputColumn:
    in_name: str
    out_name: str
    format_fn: Callable = date_else_identity
    getter: Callable = None


def column(name):
    return OutputColumn(in_name=name, out_name=name)


def mapped_column(in_name, out_name):
    return OutputColumn(in_name=in_name, out_name=out_name)


def subtable(ctx, in_name, columns, out_name=None, subobject_name=None):
    if not out_name:
        out_name = in_name

    def format_fn(records):
        return format_table(ctx, records, columns)

    def getter(record, base_getter):
        subobject = base_getter(subobject_name)(record)
        return base_getter(in_name)(subobject)

    col_getter = None
    if subobject_name:
        col_getter = getter

    return OutputColumn(
        in_name=in_name, out_name=out_name, format_fn=format_fn, getter=col_getter
    )


def subobject_column(in_name, out_name, subobject_name):
    if not out_name:
        out_name = in_name

    def getter(record, base_getter):
        subobject = base_getter(subobject_name)(record)
        return base_getter(in_name)(subobject)

    return OutputColumn(in_name=in_name, out_name=out_name, getter=getter)


def metadata_column(in_name, out_name=None):
    return subobject_column(in_name, out_name, "metadata")


def spec_column(in_name, out_name=None):
    return subobject_column(in_name, out_name, "spec")


def status_column(in_name, out_name=None):
    return subobject_column(in_name, out_name, "status")


def format_table(ctx, records, columns, getter=operator.attrgetter):
    if context.output_json(ctx):
        records_as_dicts = [
            record.to_dict() if not isinstance(record, dict) else record
            for record in records
        ]
        return convert_to_json(ctx, records_as_dicts)

    table = PrettyTable([column.out_name for column in columns])
    if not records:
        return table

    for record in records:
        row = []
        for column in columns:
            in_value = None
            if column.getter:
                in_value = column.getter(record, getter)
            else:
                in_value = getter(column.in_name)(record)

            out_value = "---"
            if in_value is not None:
                out_value = column.format_fn(in_value)
            row.append(out_value)

        table.add_row(row)
    table.align = "l"
    return table
