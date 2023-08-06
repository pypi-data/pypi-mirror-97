from . import context
from .input_helpers import get_org_from_input_or_ctx
from .output.table import (
    format_table,
    metadata_column,
    spec_column,
)
import agilicus


def query_permissions(ctx, org_id=None, **kwargs):
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    query_results = apiclient.permissions_api.list_resource_permissions(
        org_id=org_id, **kwargs
    )
    if query_results:
        return query_results.resource_permissions
    return []


def format_permissions(ctx, roles):
    columns = [
        metadata_column("id"),
        spec_column("resource_type", "type"),
        spec_column("user_id", "user id"),
        spec_column("org_id", "org id"),
        spec_column("resource_id", "resource id"),
        spec_column("resource_role_name", "role"),
    ]
    return format_table(ctx, roles, columns)


def add_permission(
    ctx, user_id, resource_id, resource_type, resource_role_name, org_id=None
):
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    spec = agilicus.ResourcePermissionSpec(
        org_id=org_id,
        user_id=user_id,
        resource_type=resource_type,
        resource_role_name=resource_role_name,
        resource_id=resource_id,
    )
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    return apiclient.permissions_api.create_resource_permission(
        agilicus.ResourcePermission(spec=spec)
    ).to_dict()


def delete_permission(ctx, id, org_id=None):
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    return apiclient.permissions_api.delete_resource_permission(id, org_id=org_id)
