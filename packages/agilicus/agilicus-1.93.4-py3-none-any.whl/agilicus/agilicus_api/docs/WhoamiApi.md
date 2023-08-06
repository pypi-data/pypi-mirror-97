# agilicus_api.WhoamiApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_whoami**](WhoamiApi.md#create_whoami) | **POST** /v1/whoami | login through whoami


# **create_whoami**
> WhoamiResponse create_whoami(x_request_id, whoami_request)

login through whoami

login through whoami

### Example

```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with agilicus_api.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.WhoamiApi(api_client)
    x_request_id = '73WakrfVbNJBaAmhQtEeDv' # str | a unique shortuuid
whoami_request = agilicus_api.WhoamiRequest() # WhoamiRequest | 

    try:
        # login through whoami
        api_response = api_instance.create_whoami(x_request_id, whoami_request)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WhoamiApi->create_whoami: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_request_id** | **str**| a unique shortuuid | 
 **whoami_request** | [**WhoamiRequest**](WhoamiRequest.md)|  | 

### Return type

[**WhoamiResponse**](WhoamiResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | user logged in |  -  |
**403** | Unauthorized user |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

