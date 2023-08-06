# agilicus_api.AuditsApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**list_audits**](AuditsApi.md#list_audits) | **GET** /v1/audits | View audit records
[**list_auth_records**](AuditsApi.md#list_auth_records) | **GET** /v1/auth_audits | View authentication audit records


# **list_audits**
> ListAuditsResponse list_audits(limit=limit, user_id=user_id, dt_from=dt_from, dt_to=dt_to, action=action, target_id=target_id, token_id=token_id, api_name=api_name, target_resource_type=target_resource_type, org_id=org_id)

View audit records

View audit records for any API

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.AuditsApi(api_client)
    limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
user_id = '1234' # str | Query based on user id (optional)
dt_from = '' # str | Search criteria from when the query happened. * Inclusive. * In UTC. * Supports human-friendly values such as \"now\", \"today\", \"now-1day\".  (optional) (default to '')
dt_to = '' # str | Search criteria until when the query happened. * Exclusive. * In UTC. * Supports human-friendly values such as \"now\", \"today\", \"now-1day\".  (optional) (default to '')
action = '' # str | the type of action which caused the log (optional) (default to '')
target_id = '' # str | The identifier for the target of the log (e.g. the jti of a created token).  (optional) (default to '')
token_id = 'token_id_example' # str | The id of the bearer token for which to find records. (optional)
api_name = '' # str | The name of the API which generated the audit logs (optional) (default to '')
target_resource_type = '' # str | Filters the type of resource associated with the audit records. (optional) (default to '')
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # View audit records
        api_response = api_instance.list_audits(limit=limit, user_id=user_id, dt_from=dt_from, dt_to=dt_to, action=action, target_id=target_id, token_id=token_id, api_name=api_name, target_resource_type=target_resource_type, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AuditsApi->list_audits: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **user_id** | **str**| Query based on user id | [optional] 
 **dt_from** | **str**| Search criteria from when the query happened. * Inclusive. * In UTC. * Supports human-friendly values such as \&quot;now\&quot;, \&quot;today\&quot;, \&quot;now-1day\&quot;.  | [optional] [default to &#39;&#39;]
 **dt_to** | **str**| Search criteria until when the query happened. * Exclusive. * In UTC. * Supports human-friendly values such as \&quot;now\&quot;, \&quot;today\&quot;, \&quot;now-1day\&quot;.  | [optional] [default to &#39;&#39;]
 **action** | **str**| the type of action which caused the log | [optional] [default to &#39;&#39;]
 **target_id** | **str**| The identifier for the target of the log (e.g. the jti of a created token).  | [optional] [default to &#39;&#39;]
 **token_id** | **str**| The id of the bearer token for which to find records. | [optional] 
 **api_name** | **str**| The name of the API which generated the audit logs | [optional] [default to &#39;&#39;]
 **target_resource_type** | **str**| Filters the type of resource associated with the audit records. | [optional] [default to &#39;&#39;]
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**ListAuditsResponse**](ListAuditsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The query ran without error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_auth_records**
> ListAuthAuditsResponse list_auth_records(limit=limit, user_id=user_id, dt_from=dt_from, dt_to=dt_to, org_id=org_id, session_id=session_id, trace_id=trace_id, upstream_user_id=upstream_user_id, upstream_idp=upstream_idp, login_org_id=login_org_id, source_ip=source_ip, client_id=client_id, event=event, stage=stage)

View authentication audit records

View and search authentication audit records for different users and organisations in the system. 

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.AuditsApi(api_client)
    limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
user_id = '1234' # str | Query based on user id (optional)
dt_from = '' # str | Search criteria from when the query happened. * Inclusive. * In UTC. * Supports human-friendly values such as \"now\", \"today\", \"now-1day\".  (optional) (default to '')
dt_to = '' # str | Search criteria until when the query happened. * Exclusive. * In UTC. * Supports human-friendly values such as \"now\", \"today\", \"now-1day\".  (optional) (default to '')
org_id = '1234' # str | Organisation Unique identifier (optional)
session_id = '1234' # str | The session formed when the user started to log in. (optional)
trace_id = '1234-abcd' # str | The id representing the request that triggered the event (optional)
upstream_user_id = '1234-abcd' # str | The id of the user from upstream (optional)
upstream_idp = 'google' # str | The name of the upstream idp (optional)
login_org_id = '1234' # str | The org id the user tried to log in to (optional)
source_ip = '192.0.2.3' # str | The source IP address of the client device logging in. (optional)
client_id = 'my-client-123' # str | The oidc client id used to log in (optional)
event = 'Success' # str | The event which triggered the audit record (optional)
stage = 'Login' # str | The stage of a pipeline to query for (optional)

    try:
        # View authentication audit records
        api_response = api_instance.list_auth_records(limit=limit, user_id=user_id, dt_from=dt_from, dt_to=dt_to, org_id=org_id, session_id=session_id, trace_id=trace_id, upstream_user_id=upstream_user_id, upstream_idp=upstream_idp, login_org_id=login_org_id, source_ip=source_ip, client_id=client_id, event=event, stage=stage)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AuditsApi->list_auth_records: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **user_id** | **str**| Query based on user id | [optional] 
 **dt_from** | **str**| Search criteria from when the query happened. * Inclusive. * In UTC. * Supports human-friendly values such as \&quot;now\&quot;, \&quot;today\&quot;, \&quot;now-1day\&quot;.  | [optional] [default to &#39;&#39;]
 **dt_to** | **str**| Search criteria until when the query happened. * Exclusive. * In UTC. * Supports human-friendly values such as \&quot;now\&quot;, \&quot;today\&quot;, \&quot;now-1day\&quot;.  | [optional] [default to &#39;&#39;]
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **session_id** | **str**| The session formed when the user started to log in. | [optional] 
 **trace_id** | **str**| The id representing the request that triggered the event | [optional] 
 **upstream_user_id** | **str**| The id of the user from upstream | [optional] 
 **upstream_idp** | **str**| The name of the upstream idp | [optional] 
 **login_org_id** | **str**| The org id the user tried to log in to | [optional] 
 **source_ip** | **str**| The source IP address of the client device logging in. | [optional] 
 **client_id** | **str**| The oidc client id used to log in | [optional] 
 **event** | **str**| The event which triggered the audit record | [optional] 
 **stage** | **str**| The stage of a pipeline to query for | [optional] 

### Return type

[**ListAuthAuditsResponse**](ListAuthAuditsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The query ran without error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

