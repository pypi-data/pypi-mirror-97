import json

import requests

from . import context, response

from .input_helpers import get_org_from_input_or_ctx
from agilicus import OpenApiException
from agilicus.agilicus_api import FeatureFlag


def get_org_by_dictionary(ctx, org_id):
    if org_id:
        data = [get(ctx, org_id)]
    else:
        data = query(ctx, org_id)

    org_dict_by_id = {}
    org_dict_by_name = {}
    for org in data:
        if not org:
            continue
        org_dict_by_id[org["id"]] = org
        org_dict_by_name[org["organisation"]] = org
    return (org_dict_by_id, org_dict_by_name)


def query(ctx, org_id=None, organisation=None, issuer=None, **kwargs):
    token = context.get_token(ctx)

    org_id = get_org_from_input_or_ctx(ctx, org_id)

    params = {}
    params["organisation"] = organisation
    params["issuer"] = issuer

    if org_id:
        params["org_id"] = org_id
        params["list_children"] = True

    apiclient = context.get_apiclient(ctx, token)
    resp = apiclient.org_api.list_orgs(**params)

    return resp.to_dict()["orgs"]


def query_suborgs(ctx, org_id=None, **kwargs):
    token = context.get_token(ctx)
    if not org_id:
        org_id = context.get_org_id(ctx, token)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)

    uri = f"/v1/orgs/{org_id}/orgs"
    resp = requests.get(
        context.get_api(ctx) + uri,
        headers=headers,
        verify=context.get_cacert(ctx),
    )
    response.validate(resp)
    return json.loads(resp.text)["orgs"]


def get_raw(ctx, org_id):
    apiclient = context.get_apiclient(ctx)
    org = apiclient.org_api.get_org(org_id=org_id)
    return org


def get(ctx, org_id, org=None):
    try:
        return get_raw(ctx, org_id).to_dict()
    except OpenApiException:
        return None


def update(
    ctx,
    org_id,
    auto_create=None,
    issuer=None,
    issuer_id=None,
    contact_id=None,
    subdomain=None,
    external_id=None,
    trust_on_first_use_duration=None,
    admin_state=None,
    name_slug=None,
):
    token = context.get_token(ctx)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)
    headers["content-type"] = "application/json"

    data = get(ctx, org_id)

    del data["created"]
    if "updated" in data:
        del data["updated"]

    del data["id"]
    del data["issuer"]

    if "sub_organisations" in data:
        del data["sub_organisations"]

    if "sub_orgs" in data:
        del data["sub_orgs"]

    if auto_create is not None:
        data["auto_create"] = auto_create

    if contact_id:
        data["contact_id"] = contact_id

    if subdomain:
        data["subdomain"] = subdomain

    if external_id:
        data["external_id"] = external_id

    if issuer is not None:
        data["issuer"] = issuer

    if issuer_id is not None:
        data["issuer_id"] = issuer_id

    if trust_on_first_use_duration is not None:
        data["trust_on_first_use_duration"] = trust_on_first_use_duration

    if admin_state is not None:
        data["admin_state"] = admin_state

    if name_slug is not None:
        data["name_slug"] = name_slug

    for i in list(data):
        if data[i] is None:
            del data[i]

    uri = "/v1/orgs/{}".format(org_id)
    resp = requests.put(
        context.get_api(ctx) + uri,
        headers=headers,
        data=json.dumps(data),
        verify=context.get_cacert(ctx),
    )
    response.validate(resp)
    return resp.text


def add(
    ctx,
    organisation,
    issuer,
    issuer_id,
    contact_id=None,
    auto_create=True,
    subdomain=None,
):
    token = context.get_token(ctx)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)
    headers["content-type"] = "application/json"

    data = {}
    data["organisation"] = organisation
    data["issuer"] = issuer
    if issuer_id:
        data["issuer_id"] = issuer_id
    if contact_id:
        data["contact_id"] = contact_id
    if subdomain:
        data["subdomain"] = subdomain
    data["auto_create"] = auto_create

    uri = "/v1/orgs"
    resp = requests.post(
        context.get_api(ctx) + uri,
        headers=headers,
        data=json.dumps(data),
        verify=context.get_cacert(ctx),
    )
    response.validate(resp)
    return json.loads(resp.text)


def add_suborg(
    ctx, organisation, contact_id=None, auto_create=True, subdomain=None, org_id=None
):
    token = context.get_token(ctx)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)
    headers["content-type"] = "application/json"

    data = {}
    data["organisation"] = organisation
    if contact_id:
        data["contact_id"] = contact_id
    if subdomain:
        data["subdomain"] = subdomain
    data["auto_create"] = auto_create

    org_id = org_id or context.get_org_id(ctx, token)
    uri = f"/v1/orgs/{org_id}/orgs"
    resp = requests.post(
        context.get_api(ctx) + uri,
        headers=headers,
        data=json.dumps(data),
        verify=context.get_cacert(ctx),
    )
    response.validate(resp)
    return json.loads(resp.text)


def delete_suborg(ctx, suborg_id):
    token = context.get_token(ctx)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)
    headers["content-type"] = "application/json"

    uri = "/v1/orgs/{}/orgs/{}".format(context.get_org_id(ctx, token), suborg_id)
    resp = requests.delete(
        context.get_api(ctx) + uri,
        headers=headers,
        verify=context.get_cacert(ctx),
    )
    response.validate(resp)


def delete(ctx, org_id):
    token = context.get_token(ctx)

    headers = {}
    headers["Authorization"] = "Bearer {}".format(token)
    headers["content-type"] = "application/json"

    uri = "/v1/orgs/{}".format(org_id)
    resp = requests.delete(
        context.get_api(ctx) + uri,
        headers=headers,
        verify=context.get_cacert(ctx),
    )
    response.validate(resp)
    return json.loads(resp.text)


def find_feature(features, feature_name):
    for feature in features:
        if feature.feature == feature_name:
            return feature

    return None


def set_feature(ctx, feature, enabled, setting="", **kwargs):
    apiclient = context.get_apiclient(ctx)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    org = get_raw(ctx, org_id)
    features = org.feature_flags or []
    feature_obj = find_feature(features, feature)

    if not feature_obj:
        feature_obj = FeatureFlag(feature=feature, enabled=enabled, setting=setting)
    else:
        # not the most efficient but simple enough.
        features.remove(feature_obj)

    feature_obj.enabled = enabled
    feature_obj.setting = setting

    features.append(feature_obj)

    org.feature_flags = features

    apiclient.org_api.replace_org(org_id=org.id, organisation=org)
    return get_raw(ctx, org_id).to_dict()


def remove_feature(ctx, feature, **kwargs):
    apiclient = context.get_apiclient(ctx)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    org = get_raw(ctx, org_id)
    features = org.feature_flags or []
    feature_obj = find_feature(features, feature)
    if not feature_obj:
        return org.to_dict()

    features.remove(feature_obj)

    org.feature_flags = features

    apiclient.org_api.replace_org(org_id=org.id, organisation=org)
    return get_raw(ctx, org_id).to_dict()
