# agilicus_api.ServicesApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_service**](ServicesApi.md#create_service) | **POST** /v2/services | Create a Service
[**delete_service**](ServicesApi.md#delete_service) | **DELETE** /v2/services/{service_id} | Remove a Service
[**get_service**](ServicesApi.md#get_service) | **GET** /v2/services/{service_id} | Get a single Service
[**list_services**](ServicesApi.md#list_services) | **GET** /v2/services | Get a subset of the Services
[**replace_service**](ServicesApi.md#replace_service) | **PUT** /v2/services/{service_id} | Create or update a Service.


# **create_service**
> Service create_service(service)

Create a Service

Creates a new Service. Note that the Service's name must be unique across all other services an Applications, regardless of the Organisation. 

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
    api_instance = agilicus_api.ServicesApi(api_client)
    service = agilicus_api.Service() # Service | 

    try:
        # Create a Service
        api_response = api_instance.create_service(service)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ServicesApi->create_service: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service** | [**Service**](Service.md)|  | 

### Return type

[**Service**](Service.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New Service created |  -  |
**409** | A Service with the same name already exists for this organisation. The existing Service is returned.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_service**
> delete_service(service_id, org_id)

Remove a Service

Remove a Service

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
    api_instance = agilicus_api.ServicesApi(api_client)
    service_id = 'service_id_example' # str | Service unique identifier
org_id = 'org_id_example' # str | Organisation unique identifier

    try:
        # Remove a Service
        api_instance.delete_service(service_id, org_id)
    except ApiException as e:
        print("Exception when calling ServicesApi->delete_service: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service_id** | **str**| Service unique identifier | 
 **org_id** | **str**| Organisation unique identifier | 

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Service was deleted |  -  |
**404** | Service does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_service**
> Service get_service(service_id)

Get a single Service

Get a single Service

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
    api_instance = agilicus_api.ServicesApi(api_client)
    service_id = 'service_id_example' # str | Service unique identifier

    try:
        # Get a single Service
        api_response = api_instance.get_service(service_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ServicesApi->get_service: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service_id** | **str**| Service unique identifier | 

### Return type

[**Service**](Service.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The Service was found. |  -  |
**404** | The Service does not exist. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_services**
> ListServicesResponse list_services(org_id=org_id)

Get a subset of the Services

Retrieves all Services owned by the Organisation.

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
    api_instance = agilicus_api.ServicesApi(api_client)
    org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Get a subset of the Services
        api_response = api_instance.list_services(org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ServicesApi->list_services: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**ListServicesResponse**](ListServicesResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The list of retrieved Services |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_service**
> Service replace_service(service_id, service=service)

Create or update a Service.

Create or update a Service.

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
    api_instance = agilicus_api.ServicesApi(api_client)
    service_id = 'service_id_example' # str | Service unique identifier
service = agilicus_api.Service() # Service |  (optional)

    try:
        # Create or update a Service.
        api_response = api_instance.replace_service(service_id, service=service)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ServicesApi->replace_service: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service_id** | **str**| Service unique identifier | 
 **service** | [**Service**](Service.md)|  | [optional] 

### Return type

[**Service**](Service.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The Service was updated. Returns the latest version of it after the update was applied.  |  -  |
**404** | Service does not exist. |  -  |
**409** | The provided Service conflicted with the value stored in the API. Please fetch the latest version and try again with it.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

