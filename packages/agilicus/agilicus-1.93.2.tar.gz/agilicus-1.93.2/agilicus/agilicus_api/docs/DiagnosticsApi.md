# agilicus_api.DiagnosticsApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**list_logs**](DiagnosticsApi.md#list_logs) | **GET** /v1/diagnostics/logs | Retrieve application logs


# **list_logs**
> ListLogsResponse list_logs(org_id, dt_from=dt_from, dt_to=dt_to, app=app, sub=sub, limit=limit, sub_org_id=sub_org_id, env=env, dt_sort=dt_sort)

Retrieve application logs

Retrieve application diagnostic logs. These are the output from stdout/stderr (stream). 

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
    api_instance = agilicus_api.DiagnosticsApi(api_client)
    org_id = 'org_id_example' # str | query for a specific organization
dt_from = 'dt_from_example' # str | search criteria, search logs from (optional)
dt_to = 'dt_to_example' # str | search criteria, search logs to (optional)
app = 'app_example' # str | search criteria, search logs for an app (optional)
sub = 'sub_example' # str | search criteria, search logs for a given subject (USER) GUID (optional)
limit = 150 # int | limit number of output logs (optional) (default to 150)
sub_org_id = 'sub_org_id_example' # str | query for a specific sub-organization (optional)
env = 'env_example' # str | query for a specific environment (optional)
dt_sort = 'dt_sort_example' # str | Sort order: *'asc' - ascending, from old to new logs *'desc' - descending, from new to old logs  (optional)

    try:
        # Retrieve application logs
        api_response = api_instance.list_logs(org_id, dt_from=dt_from, dt_to=dt_to, app=app, sub=sub, limit=limit, sub_org_id=sub_org_id, env=env, dt_sort=dt_sort)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DiagnosticsApi->list_logs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| query for a specific organization | 
 **dt_from** | **str**| search criteria, search logs from | [optional] 
 **dt_to** | **str**| search criteria, search logs to | [optional] 
 **app** | **str**| search criteria, search logs for an app | [optional] 
 **sub** | **str**| search criteria, search logs for a given subject (USER) GUID | [optional] 
 **limit** | **int**| limit number of output logs | [optional] [default to 150]
 **sub_org_id** | **str**| query for a specific sub-organization | [optional] 
 **env** | **str**| query for a specific environment | [optional] 
 **dt_sort** | **str**| Sort order: *&#39;asc&#39; - ascending, from old to new logs *&#39;desc&#39; - descending, from new to old logs  | [optional] 

### Return type

[**ListLogsResponse**](ListLogsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return logs in JSON format for specified parameters |  -  |
**400** | Query is invalid |  -  |
**401** | Unauthorized access |  -  |
**403** | User does not have permissions to query |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

