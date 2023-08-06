# agilicus_api.GroupsApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_group_member**](GroupsApi.md#add_group_member) | **POST** /v1/groups/{group_id}/members | Add a group member
[**create_group**](GroupsApi.md#create_group) | **POST** /v1/groups | Create a group
[**delete_group**](GroupsApi.md#delete_group) | **DELETE** /v1/groups/{group_id} | Delete a group
[**delete_group_member**](GroupsApi.md#delete_group_member) | **DELETE** /v1/groups/{group_id}/members/{member_id} | Remove a group member
[**get_group**](GroupsApi.md#get_group) | **GET** /v1/groups/{group_id} | Get a group
[**list_groups**](GroupsApi.md#list_groups) | **GET** /v1/groups | Get all groups
[**replace_group**](GroupsApi.md#replace_group) | **PUT** /v1/groups/{group_id} | update a group


# **add_group_member**
> User add_group_member(group_id, add_group_member_request)

Add a group member

Add a group member

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
    api_instance = agilicus_api.GroupsApi(api_client)
    group_id = '1234' # str | group_id path
add_group_member_request = agilicus_api.AddGroupMemberRequest() # AddGroupMemberRequest | 

    try:
        # Add a group member
        api_response = api_instance.add_group_member(group_id, add_group_member_request)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->add_group_member: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_id** | **str**| group_id path | 
 **add_group_member_request** | [**AddGroupMemberRequest**](AddGroupMemberRequest.md)|  | 

### Return type

[**User**](User.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New group member added |  -  |
**409** | Group member already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_group**
> Group create_group(group)

Create a group

Create a group

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
    api_instance = agilicus_api.GroupsApi(api_client)
    group = agilicus_api.Group() # Group | 

    try:
        # Create a group
        api_response = api_instance.create_group(group)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->create_group: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group** | [**Group**](Group.md)|  | 

### Return type

[**Group**](Group.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New group created |  -  |
**409** | Group already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_group**
> delete_group(group_id, org_id=org_id)

Delete a group

Delete a group

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
    api_instance = agilicus_api.GroupsApi(api_client)
    group_id = '1234' # str | group_id path
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Delete a group
        api_instance.delete_group(group_id, org_id=org_id)
    except ApiException as e:
        print("Exception when calling GroupsApi->delete_group: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_id** | **str**| group_id path | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

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
**204** | Group was deleted |  -  |
**404** | Group does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_group_member**
> delete_group_member(group_id, member_id, org_id=org_id)

Remove a group member

Remove a group member

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
    api_instance = agilicus_api.GroupsApi(api_client)
    group_id = '1234' # str | group_id path
member_id = '1234' # str | member_id path
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Remove a group member
        api_instance.delete_group_member(group_id, member_id, org_id=org_id)
    except ApiException as e:
        print("Exception when calling GroupsApi->delete_group_member: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_id** | **str**| group_id path | 
 **member_id** | **str**| member_id path | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

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
**204** | member was removed |  -  |
**404** | group or member does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_group**
> Group get_group(group_id, org_id=org_id)

Get a group

Get a group

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
    api_instance = agilicus_api.GroupsApi(api_client)
    group_id = '1234' # str | group_id path
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Get a group
        api_response = api_instance.get_group(group_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->get_group: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_id** | **str**| group_id path | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**Group**](Group.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return group |  -  |
**404** | Group does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_groups**
> ListGroupsResponse list_groups(org_id=org_id, type=type, limit=limit, previous_email=previous_email, search_direction=search_direction, prefix_email_search=prefix_email_search, allow_partial_match=allow_partial_match, first_name=first_name, last_name=last_name, search_params=search_params)

Get all groups

Get all groups

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
    api_instance = agilicus_api.GroupsApi(api_client)
    org_id = '1234' # str | Organisation Unique identifier (optional)
type = ["group"] # list[str] | The type of groups to search for. Multiple values are ORed together. (optional) (default to ["group"])
limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
previous_email = 'foo@example.com' # str | Pagination based query with the user's email as the key. To get the initial entries supply an empty string. (optional)
search_direction = 'forwards' # str | Direction which the search should go starting from the email_nullable_query parameter.  (optional) (default to 'forwards')
prefix_email_search = 'Foo' # str | Keyword used to search for a list of users based on email. This parameter is case insensitive and finds users with an email that matches the keyword by its prefix. For example, if the keyword \"Foo\" is supplied to this parameter, users with emails of \"foo1@example.com\" and \"Foo2@test.com\" could be returned.  (optional)
allow_partial_match = True # bool | Perform a case insensitive partial match of any string query parameters included in the query  (optional)
first_name = 'John' # str | query for users with a first name that matches the query parameter (optional)
last_name = 'Smith' # str | query for users with a last name that matches the query parameter (optional)
search_params = ['mat'] # list[str] | A list of strings to perform a case-insensitive search on all relevant fields in the database for a given collection. Multiple values are ANDed together  (optional)

    try:
        # Get all groups
        api_response = api_instance.list_groups(org_id=org_id, type=type, limit=limit, previous_email=previous_email, search_direction=search_direction, prefix_email_search=prefix_email_search, allow_partial_match=allow_partial_match, first_name=first_name, last_name=last_name, search_params=search_params)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->list_groups: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **type** | [**list[str]**](str.md)| The type of groups to search for. Multiple values are ORed together. | [optional] [default to [&quot;group&quot;]]
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **previous_email** | **str**| Pagination based query with the user&#39;s email as the key. To get the initial entries supply an empty string. | [optional] 
 **search_direction** | **str**| Direction which the search should go starting from the email_nullable_query parameter.  | [optional] [default to &#39;forwards&#39;]
 **prefix_email_search** | **str**| Keyword used to search for a list of users based on email. This parameter is case insensitive and finds users with an email that matches the keyword by its prefix. For example, if the keyword \&quot;Foo\&quot; is supplied to this parameter, users with emails of \&quot;foo1@example.com\&quot; and \&quot;Foo2@test.com\&quot; could be returned.  | [optional] 
 **allow_partial_match** | **bool**| Perform a case insensitive partial match of any string query parameters included in the query  | [optional] 
 **first_name** | **str**| query for users with a first name that matches the query parameter | [optional] 
 **last_name** | **str**| query for users with a last name that matches the query parameter | [optional] 
 **search_params** | [**list[str]**](str.md)| A list of strings to perform a case-insensitive search on all relevant fields in the database for a given collection. Multiple values are ANDed together  | [optional] 

### Return type

[**ListGroupsResponse**](ListGroupsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return groups |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_group**
> Group replace_group(group_id, group=group)

update a group

update a group

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
    api_instance = agilicus_api.GroupsApi(api_client)
    group_id = '1234' # str | group_id path
group = agilicus_api.Group() # Group |  (optional)

    try:
        # update a group
        api_response = api_instance.replace_group(group_id, group=group)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling GroupsApi->replace_group: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_id** | **str**| group_id path | 
 **group** | [**Group**](Group.md)|  | [optional] 

### Return type

[**Group**](Group.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return updated group |  -  |
**404** | group does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

