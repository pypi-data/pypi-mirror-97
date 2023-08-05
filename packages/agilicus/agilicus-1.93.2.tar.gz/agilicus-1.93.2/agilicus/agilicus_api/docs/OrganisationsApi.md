# agilicus_api.OrganisationsApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_blocking_upgrade_orgs_task**](OrganisationsApi.md#create_blocking_upgrade_orgs_task) | **POST** /v1/orgs/upgrade | utility to upgrade organisations
[**create_org**](OrganisationsApi.md#create_org) | **POST** /v1/orgs | Create an organisation
[**create_sub_org**](OrganisationsApi.md#create_sub_org) | **POST** /v1/orgs/{org_id}/orgs | Create a sub organisation
[**delete_sub_org**](OrganisationsApi.md#delete_sub_org) | **DELETE** /v1/orgs/{org_id}/orgs/{sub_org_id} | Delete a sub organisation
[**get_org**](OrganisationsApi.md#get_org) | **GET** /v1/orgs/{org_id} | Get a single organisation
[**get_org_status**](OrganisationsApi.md#get_org_status) | **GET** /v1/orgs/{org_id}/status | Get the status of an organisation
[**list_orgs**](OrganisationsApi.md#list_orgs) | **GET** /v1/orgs | Get all organisations
[**list_sub_orgs**](OrganisationsApi.md#list_sub_orgs) | **GET** /v1/orgs/{org_id}/orgs | Get all sub organisations
[**replace_org**](OrganisationsApi.md#replace_org) | **PUT** /v1/orgs/{org_id} | Create or update an organisation


# **create_blocking_upgrade_orgs_task**
> create_blocking_upgrade_orgs_task()

utility to upgrade organisations

utility to upgrade organisations

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
    api_instance = agilicus_api.OrganisationsApi(api_client)
    
    try:
        # utility to upgrade organisations
        api_instance.create_blocking_upgrade_orgs_task()
    except ApiException as e:
        print("Exception when calling OrganisationsApi->create_blocking_upgrade_orgs_task: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

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
**204** | organisations upgraded |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_org**
> Organisation create_org(organisation_admin)

Create an organisation

Create an organisation

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
    api_instance = agilicus_api.OrganisationsApi(api_client)
    organisation_admin = agilicus_api.OrganisationAdmin() # OrganisationAdmin | 

    try:
        # Create an organisation
        api_response = api_instance.create_org(organisation_admin)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganisationsApi->create_org: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organisation_admin** | [**OrganisationAdmin**](OrganisationAdmin.md)|  | 

### Return type

[**Organisation**](Organisation.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New organisation created |  -  |
**400** | New organisation created |  -  |
**409** | Organisation already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_sub_org**
> Organisation create_sub_org(org_id, organisation)

Create a sub organisation

Create a sub organisation

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
    api_instance = agilicus_api.OrganisationsApi(api_client)
    org_id = '1234' # str | Organisation Unique identifier
organisation = agilicus_api.Organisation() # Organisation | 

    try:
        # Create a sub organisation
        api_response = api_instance.create_sub_org(org_id, organisation)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganisationsApi->create_sub_org: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | 
 **organisation** | [**Organisation**](Organisation.md)|  | 

### Return type

[**Organisation**](Organisation.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New sub organisation created |  -  |
**409** | Organisation already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_sub_org**
> delete_sub_org(org_id, sub_org_id)

Delete a sub organisation

Delete a sub organisation

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
    api_instance = agilicus_api.OrganisationsApi(api_client)
    org_id = '1234' # str | Organisation Unique identifier
sub_org_id = '1234' # str | Sub Organisation Unique identifier

    try:
        # Delete a sub organisation
        api_instance.delete_sub_org(org_id, sub_org_id)
    except ApiException as e:
        print("Exception when calling OrganisationsApi->delete_sub_org: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | 
 **sub_org_id** | **str**| Sub Organisation Unique identifier | 

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
**204** | Organisation was deleted |  -  |
**404** | Organisation does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_org**
> Organisation get_org(org_id)

Get a single organisation

Get a single organisation

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
    api_instance = agilicus_api.OrganisationsApi(api_client)
    org_id = '1234' # str | Organisation Unique identifier

    try:
        # Get a single organisation
        api_response = api_instance.get_org(org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganisationsApi->get_org: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | 

### Return type

[**Organisation**](Organisation.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return organisation |  -  |
**404** | Organisation does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_org_status**
> OrganisationStatus get_org_status(org_id)

Get the status of an organisation

Get the status of an organisation

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
    api_instance = agilicus_api.OrganisationsApi(api_client)
    org_id = '1234' # str | Organisation Unique identifier

    try:
        # Get the status of an organisation
        api_response = api_instance.get_org_status(org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganisationsApi->get_org_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | 

### Return type

[**OrganisationStatus**](OrganisationStatus.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return organisation status |  -  |
**404** | Organisation does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_orgs**
> ListOrgsResponse list_orgs(limit=limit, org_id=org_id, organisation=organisation, issuer=issuer, list_children=list_children, updated_since=updated_since, suborg_updated=suborg_updated)

Get all organisations

Get all organisations

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
    api_instance = agilicus_api.OrganisationsApi(api_client)
    limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
org_id = '1234' # str | Organisation Unique identifier (optional)
organisation = 'agilicus' # str | Organisation Name (optional)
issuer = 'example.com' # str | Organisation issuer (optional)
list_children = False # bool | Controls whether or not children of the matching resources are returned in the listing.  (optional) (default to False)
updated_since = '2015-07-07T15:49:51.230+02:00' # datetime | query since updated (optional)
suborg_updated = true # bool | query any orgs who are updated or have their suborgs updated (optional)

    try:
        # Get all organisations
        api_response = api_instance.list_orgs(limit=limit, org_id=org_id, organisation=organisation, issuer=issuer, list_children=list_children, updated_since=updated_since, suborg_updated=suborg_updated)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganisationsApi->list_orgs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **organisation** | **str**| Organisation Name | [optional] 
 **issuer** | **str**| Organisation issuer | [optional] 
 **list_children** | **bool**| Controls whether or not children of the matching resources are returned in the listing.  | [optional] [default to False]
 **updated_since** | **datetime**| query since updated | [optional] 
 **suborg_updated** | **bool**| query any orgs who are updated or have their suborgs updated | [optional] 

### Return type

[**ListOrgsResponse**](ListOrgsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return organisations |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_sub_orgs**
> ListOrgsResponse list_sub_orgs(org_id, limit=limit, updated_since=updated_since)

Get all sub organisations

Get all sub organisations

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
    api_instance = agilicus_api.OrganisationsApi(api_client)
    org_id = '1234' # str | Organisation Unique identifier
limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
updated_since = '2015-07-07T15:49:51.230+02:00' # datetime | query since updated (optional)

    try:
        # Get all sub organisations
        api_response = api_instance.list_sub_orgs(org_id, limit=limit, updated_since=updated_since)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling OrganisationsApi->list_sub_orgs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | 
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **updated_since** | **datetime**| query since updated | [optional] 

### Return type

[**ListOrgsResponse**](ListOrgsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return sub-organisations |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_org**
> replace_org(org_id, organisation=organisation)

Create or update an organisation

Create or update an organisation

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
    api_instance = agilicus_api.OrganisationsApi(api_client)
    org_id = '1234' # str | Organisation Unique identifier
organisation = agilicus_api.Organisation() # Organisation |  (optional)

    try:
        # Create or update an organisation
        api_instance.replace_org(org_id, organisation=organisation)
    except ApiException as e:
        print("Exception when calling OrganisationsApi->replace_org: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | 
 **organisation** | [**Organisation**](Organisation.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Organisation updated |  -  |
**404** | Organisation does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

