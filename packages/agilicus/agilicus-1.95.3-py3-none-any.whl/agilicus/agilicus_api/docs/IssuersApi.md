# agilicus_api.IssuersApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_client**](IssuersApi.md#create_client) | **POST** /v1/clients | Create a client
[**create_issuer**](IssuersApi.md#create_issuer) | **POST** /v1/issuers/issuer_roots | Create an issuer
[**create_policy**](IssuersApi.md#create_policy) | **POST** /v1/issuers/authentication_policies | Create a policy
[**create_policy_rule**](IssuersApi.md#create_policy_rule) | **POST** /v1/issuers/authentication_policies/{policy_id}/policy_rules | Create a policy rule
[**delete_client**](IssuersApi.md#delete_client) | **DELETE** /v1/clients/{client_id} | Delete a client
[**delete_policy**](IssuersApi.md#delete_policy) | **DELETE** /v1/issuers/authentication_policies/{policy_id} | Delete a Policy
[**delete_policy_rule**](IssuersApi.md#delete_policy_rule) | **DELETE** /v1/issuers/authentication_policies/{policy_id}/policy_rules/{policy_rule_id} | Delete a Policy Rule
[**delete_root**](IssuersApi.md#delete_root) | **DELETE** /v1/issuers/issuer_roots/{issuer_id} | Delete an Issuer
[**get_client**](IssuersApi.md#get_client) | **GET** /v1/clients/{client_id} | Get a client
[**get_issuer**](IssuersApi.md#get_issuer) | **GET** /v1/issuers/issuer_extensions/{issuer_id} | Get an issuer
[**get_policy**](IssuersApi.md#get_policy) | **GET** /v1/issuers/authentication_policies/{policy_id} | Get a policy
[**get_policy_rule**](IssuersApi.md#get_policy_rule) | **GET** /v1/issuers/authentication_policies/{policy_id}/policy_rules/{policy_rule_id} | Get a policy rule
[**get_root**](IssuersApi.md#get_root) | **GET** /v1/issuers/issuer_roots/{issuer_id} | Get an issuer
[**get_wellknown_issuer_info**](IssuersApi.md#get_wellknown_issuer_info) | **GET** /v1/issuers/issuer_extensions/{issuer_id}/well_known_info | Get well-known issuer information
[**list_clients**](IssuersApi.md#list_clients) | **GET** /v1/clients | Query Clients
[**list_issuer_roots**](IssuersApi.md#list_issuer_roots) | **GET** /v1/issuers/issuer_roots | Query Issuers
[**list_issuers**](IssuersApi.md#list_issuers) | **GET** /v1/issuers/issuer_extensions | Query Issuers
[**list_policies**](IssuersApi.md#list_policies) | **GET** /v1/issuers/authentication_policies | Query Policies
[**list_policy_rules**](IssuersApi.md#list_policy_rules) | **GET** /v1/issuers/authentication_policies/{policy_id}/policy_rules | Query Policy rules
[**list_wellknown_issuer_info**](IssuersApi.md#list_wellknown_issuer_info) | **GET** /v1/issuers/issuer_extensions/well_known_info | list well-known issuer information
[**replace_client**](IssuersApi.md#replace_client) | **PUT** /v1/clients/{client_id} | Update a client
[**replace_issuer**](IssuersApi.md#replace_issuer) | **PUT** /v1/issuers/issuer_extensions/{issuer_id} | Update an issuer
[**replace_policy**](IssuersApi.md#replace_policy) | **PUT** /v1/issuers/authentication_policies/{policy_id} | Update a policy
[**replace_policy_rule**](IssuersApi.md#replace_policy_rule) | **PUT** /v1/issuers/authentication_policies/{policy_id}/policy_rules/{policy_rule_id} | Update a policy rule
[**replace_root**](IssuersApi.md#replace_root) | **PUT** /v1/issuers/issuer_roots/{issuer_id} | Update an issuer
[**reset_to_default_policy**](IssuersApi.md#reset_to_default_policy) | **POST** /v1/issuers/issuer_extensions/{issuer_id}/set_auth_policy_to_default | Reset the current policy to the default policy


# **create_client**
> IssuerClient create_client(issuer_client)

Create a client

Create a client

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
    api_instance = agilicus_api.IssuersApi(api_client)
    issuer_client = agilicus_api.IssuerClient() # IssuerClient | IssuerClient

    try:
        # Create a client
        api_response = api_instance.create_client(issuer_client)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->create_client: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issuer_client** | [**IssuerClient**](IssuerClient.md)| IssuerClient | 

### Return type

[**IssuerClient**](IssuerClient.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully created client |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_issuer**
> Issuer create_issuer(issuer)

Create an issuer

Create an issuer

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
    api_instance = agilicus_api.IssuersApi(api_client)
    issuer = agilicus_api.Issuer() # Issuer | Issuer

    try:
        # Create an issuer
        api_response = api_instance.create_issuer(issuer)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->create_issuer: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issuer** | [**Issuer**](Issuer.md)| Issuer | 

### Return type

[**Issuer**](Issuer.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully created issuer |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_policy**
> Policy create_policy(policy)

Create a policy

Create a policy

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
    api_instance = agilicus_api.IssuersApi(api_client)
    policy = agilicus_api.Policy() # Policy | Policy

    try:
        # Create a policy
        api_response = api_instance.create_policy(policy)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->create_policy: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **policy** | [**Policy**](Policy.md)| Policy | 

### Return type

[**Policy**](Policy.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully created a Policy |  -  |
**400** | The request was invalid. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_policy_rule**
> PolicyRule create_policy_rule(policy_id, policy_rule)

Create a policy rule

Create a policy rule

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
    api_instance = agilicus_api.IssuersApi(api_client)
    policy_id = '1234' # str | Policy Unique identifier
policy_rule = agilicus_api.PolicyRule() # PolicyRule | Policy rule

    try:
        # Create a policy rule
        api_response = api_instance.create_policy_rule(policy_id, policy_rule)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->create_policy_rule: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **policy_id** | **str**| Policy Unique identifier | 
 **policy_rule** | [**PolicyRule**](PolicyRule.md)| Policy rule | 

### Return type

[**PolicyRule**](PolicyRule.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully created a Policy |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_client**
> delete_client(client_id, summarize_collection=summarize_collection, org_id=org_id)

Delete a client

Delete a client

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
    api_instance = agilicus_api.IssuersApi(api_client)
    client_id = '1234' # str | client_id path
summarize_collection = True # bool | Restrict the results to the summary. Individual collections define what content to include in the summary (optional) (default to True)
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Delete a client
        api_instance.delete_client(client_id, summarize_collection=summarize_collection, org_id=org_id)
    except ApiException as e:
        print("Exception when calling IssuersApi->delete_client: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **client_id** | **str**| client_id path | 
 **summarize_collection** | **bool**| Restrict the results to the summary. Individual collections define what content to include in the summary | [optional] [default to True]
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Client was deleted |  -  |
**404** | Issuer/Client does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_policy**
> delete_policy(policy_id, org_id=org_id)

Delete a Policy

Delete a Policy

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
    api_instance = agilicus_api.IssuersApi(api_client)
    policy_id = '1234' # str | Policy Unique identifier
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Delete a Policy
        api_instance.delete_policy(policy_id, org_id=org_id)
    except ApiException as e:
        print("Exception when calling IssuersApi->delete_policy: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **policy_id** | **str**| Policy Unique identifier | 
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
**204** | Policy was deleted |  -  |
**404** | Policy does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_policy_rule**
> delete_policy_rule(policy_id, policy_rule_id, org_id=org_id)

Delete a Policy Rule

Delete a Policy Rule

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
    api_instance = agilicus_api.IssuersApi(api_client)
    policy_id = '1234' # str | Policy Unique identifier
policy_rule_id = '1234' # str | Policy Rule Unique identifier
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Delete a Policy Rule
        api_instance.delete_policy_rule(policy_id, policy_rule_id, org_id=org_id)
    except ApiException as e:
        print("Exception when calling IssuersApi->delete_policy_rule: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **policy_id** | **str**| Policy Unique identifier | 
 **policy_rule_id** | **str**| Policy Rule Unique identifier | 
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
**204** | Policy Rule was deleted |  -  |
**404** | Policy Rule does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_root**
> delete_root(issuer_id, summarize_collection=summarize_collection)

Delete an Issuer

Delete an Issuer

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
    api_instance = agilicus_api.IssuersApi(api_client)
    issuer_id = '1234' # str | issuer_id path
summarize_collection = True # bool | Restrict the results to the summary. Individual collections define what content to include in the summary (optional) (default to True)

    try:
        # Delete an Issuer
        api_instance.delete_root(issuer_id, summarize_collection=summarize_collection)
    except ApiException as e:
        print("Exception when calling IssuersApi->delete_root: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issuer_id** | **str**| issuer_id path | 
 **summarize_collection** | **bool**| Restrict the results to the summary. Individual collections define what content to include in the summary | [optional] [default to True]

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
**204** | Issuer was deleted |  -  |
**404** | Issuer does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_client**
> IssuerClient get_client(client_id, summarize_collection=summarize_collection, org_id=org_id)

Get a client

Get a client

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
    api_instance = agilicus_api.IssuersApi(api_client)
    client_id = '1234' # str | client_id path
summarize_collection = True # bool | Restrict the results to the summary. Individual collections define what content to include in the summary (optional) (default to True)
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Get a client
        api_response = api_instance.get_client(client_id, summarize_collection=summarize_collection, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->get_client: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **client_id** | **str**| client_id path | 
 **summarize_collection** | **bool**| Restrict the results to the summary. Individual collections define what content to include in the summary | [optional] [default to True]
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**IssuerClient**](IssuerClient.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return client by id |  -  |
**404** | Client not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_issuer**
> Issuer get_issuer(issuer_id, summarize_collection=summarize_collection, org_id=org_id)

Get an issuer

Get an issuer

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
    api_instance = agilicus_api.IssuersApi(api_client)
    issuer_id = '1234' # str | issuer_id path
summarize_collection = True # bool | Restrict the results to the summary. Individual collections define what content to include in the summary (optional) (default to True)
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Get an issuer
        api_response = api_instance.get_issuer(issuer_id, summarize_collection=summarize_collection, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->get_issuer: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issuer_id** | **str**| issuer_id path | 
 **summarize_collection** | **bool**| Restrict the results to the summary. Individual collections define what content to include in the summary | [optional] [default to True]
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**Issuer**](Issuer.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return issuer by id |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_policy**
> Policy get_policy(policy_id, org_id=org_id)

Get a policy

Get a policy

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
    api_instance = agilicus_api.IssuersApi(api_client)
    policy_id = '1234' # str | Policy Unique identifier
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Get a policy
        api_response = api_instance.get_policy(policy_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->get_policy: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **policy_id** | **str**| Policy Unique identifier | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**Policy**](Policy.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return policy by id |  -  |
**404** | Policy does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_policy_rule**
> PolicyRule get_policy_rule(policy_id, policy_rule_id, org_id=org_id)

Get a policy rule

Get a policy rule

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
    api_instance = agilicus_api.IssuersApi(api_client)
    policy_id = '1234' # str | Policy Unique identifier
policy_rule_id = '1234' # str | Policy Rule Unique identifier
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Get a policy rule
        api_response = api_instance.get_policy_rule(policy_id, policy_rule_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->get_policy_rule: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **policy_id** | **str**| Policy Unique identifier | 
 **policy_rule_id** | **str**| Policy Rule Unique identifier | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**PolicyRule**](PolicyRule.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return policy rule by id |  -  |
**404** | Policy Rule does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_root**
> Issuer get_root(issuer_id, summarize_collection=summarize_collection)

Get an issuer

Get an issuer

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
    api_instance = agilicus_api.IssuersApi(api_client)
    issuer_id = '1234' # str | issuer_id path
summarize_collection = True # bool | Restrict the results to the summary. Individual collections define what content to include in the summary (optional) (default to True)

    try:
        # Get an issuer
        api_response = api_instance.get_root(issuer_id, summarize_collection=summarize_collection)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->get_root: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issuer_id** | **str**| issuer_id path | 
 **summarize_collection** | **bool**| Restrict the results to the summary. Individual collections define what content to include in the summary | [optional] [default to True]

### Return type

[**Issuer**](Issuer.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return issuer by id |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_wellknown_issuer_info**
> WellKnownIssuerInfo get_wellknown_issuer_info(issuer_id, org_id)

Get well-known issuer information

Get well-known issuer information

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
    api_instance = agilicus_api.IssuersApi(api_client)
    issuer_id = '1234' # str | issuer_id path
org_id = '1234' # str | Organisation Unique identifier

    try:
        # Get well-known issuer information
        api_response = api_instance.get_wellknown_issuer_info(issuer_id, org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->get_wellknown_issuer_info: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issuer_id** | **str**| issuer_id path | 
 **org_id** | **str**| Organisation Unique identifier | 

### Return type

[**WellKnownIssuerInfo**](WellKnownIssuerInfo.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return the issuer&#39;s well-known information |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_clients**
> ListIssuerClientsResponse list_clients(summarize_collection=summarize_collection, limit=limit, org_id=org_id)

Query Clients

Query Clients

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
    api_instance = agilicus_api.IssuersApi(api_client)
    summarize_collection = True # bool | Restrict the results to the summary. Individual collections define what content to include in the summary (optional) (default to True)
limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Query Clients
        api_response = api_instance.list_clients(summarize_collection=summarize_collection, limit=limit, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->list_clients: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **summarize_collection** | **bool**| Restrict the results to the summary. Individual collections define what content to include in the summary | [optional] [default to True]
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**ListIssuerClientsResponse**](ListIssuerClientsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return clients list |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_issuer_roots**
> ListIssuerRootsResponse list_issuer_roots(summarize_collection=summarize_collection, limit=limit, issuer=issuer)

Query Issuers

Query Issuers

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
    api_instance = agilicus_api.IssuersApi(api_client)
    summarize_collection = True # bool | Restrict the results to the summary. Individual collections define what content to include in the summary (optional) (default to True)
limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
issuer = 'example.com' # str | Organisation issuer (optional)

    try:
        # Query Issuers
        api_response = api_instance.list_issuer_roots(summarize_collection=summarize_collection, limit=limit, issuer=issuer)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->list_issuer_roots: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **summarize_collection** | **bool**| Restrict the results to the summary. Individual collections define what content to include in the summary | [optional] [default to True]
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **issuer** | **str**| Organisation issuer | [optional] 

### Return type

[**ListIssuerRootsResponse**](ListIssuerRootsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return issuers list |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_issuers**
> ListIssuerExtensionsResponse list_issuers(summarize_collection=summarize_collection, limit=limit, issuer=issuer, org_id=org_id)

Query Issuers

Query Issuers

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
    api_instance = agilicus_api.IssuersApi(api_client)
    summarize_collection = True # bool | Restrict the results to the summary. Individual collections define what content to include in the summary (optional) (default to True)
limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
issuer = 'example.com' # str | Organisation issuer (optional)
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Query Issuers
        api_response = api_instance.list_issuers(summarize_collection=summarize_collection, limit=limit, issuer=issuer, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->list_issuers: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **summarize_collection** | **bool**| Restrict the results to the summary. Individual collections define what content to include in the summary | [optional] [default to True]
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **issuer** | **str**| Organisation issuer | [optional] 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**ListIssuerExtensionsResponse**](ListIssuerExtensionsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return issuers list |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_policies**
> ListPoliciesResponse list_policies(limit=limit, org_id=org_id, issuer_id=issuer_id, policy_name=policy_name)

Query Policies

Query Policies

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
    api_instance = agilicus_api.IssuersApi(api_client)
    limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
org_id = '1234' # str | Organisation Unique identifier (optional)
issuer_id = 'abc32j3ijfn' # str | Organisation issuer id (optional)
policy_name = 'MyStrongPolicy' # str | Query the policies by name (optional)

    try:
        # Query Policies
        api_response = api_instance.list_policies(limit=limit, org_id=org_id, issuer_id=issuer_id, policy_name=policy_name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->list_policies: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **issuer_id** | **str**| Organisation issuer id | [optional] 
 **policy_name** | **str**| Query the policies by name | [optional] 

### Return type

[**ListPoliciesResponse**](ListPoliciesResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return the list of policies |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_policy_rules**
> ListPolicyRulesResponse list_policy_rules(policy_id, limit=limit, org_id=org_id)

Query Policy rules

Query Policy rules

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
    api_instance = agilicus_api.IssuersApi(api_client)
    policy_id = '1234' # str | Policy Unique identifier
limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Query Policy rules
        api_response = api_instance.list_policy_rules(policy_id, limit=limit, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->list_policy_rules: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **policy_id** | **str**| Policy Unique identifier | 
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**ListPolicyRulesResponse**](ListPolicyRulesResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return the list of policy rules |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_wellknown_issuer_info**
> ListWellKnownIssuerInfo list_wellknown_issuer_info(org_id=org_id, limit=limit)

list well-known issuer information

list well-known issuer information

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
    api_instance = agilicus_api.IssuersApi(api_client)
    org_id = '1234' # str | Organisation Unique identifier (optional)
limit = 500 # int | limit the number of rows in the response (optional) (default to 500)

    try:
        # list well-known issuer information
        api_response = api_instance.list_wellknown_issuer_info(org_id=org_id, limit=limit)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->list_wellknown_issuer_info: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]

### Return type

[**ListWellKnownIssuerInfo**](ListWellKnownIssuerInfo.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return the list of well-known issuer information |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_client**
> IssuerClient replace_client(client_id, issuer_client, summarize_collection=summarize_collection)

Update a client

Update a client

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
    api_instance = agilicus_api.IssuersApi(api_client)
    client_id = '1234' # str | client_id path
issuer_client = agilicus_api.IssuerClient() # IssuerClient | Issuer client
summarize_collection = True # bool | Restrict the results to the summary. Individual collections define what content to include in the summary (optional) (default to True)

    try:
        # Update a client
        api_response = api_instance.replace_client(client_id, issuer_client, summarize_collection=summarize_collection)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->replace_client: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **client_id** | **str**| client_id path | 
 **issuer_client** | [**IssuerClient**](IssuerClient.md)| Issuer client | 
 **summarize_collection** | **bool**| Restrict the results to the summary. Individual collections define what content to include in the summary | [optional] [default to True]

### Return type

[**IssuerClient**](IssuerClient.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Client was updated |  -  |
**400** | The request was invalid. Likely a field was missing or incorrectly formatted. |  -  |
**404** | Issuer/Client does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_issuer**
> Issuer replace_issuer(issuer_id, issuer, summarize_collection=summarize_collection)

Update an issuer

Update an issuer

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
    api_instance = agilicus_api.IssuersApi(api_client)
    issuer_id = '1234' # str | issuer_id path
issuer = agilicus_api.Issuer() # Issuer | Issuer
summarize_collection = True # bool | Restrict the results to the summary. Individual collections define what content to include in the summary (optional) (default to True)

    try:
        # Update an issuer
        api_response = api_instance.replace_issuer(issuer_id, issuer, summarize_collection=summarize_collection)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->replace_issuer: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issuer_id** | **str**| issuer_id path | 
 **issuer** | [**Issuer**](Issuer.md)| Issuer | 
 **summarize_collection** | **bool**| Restrict the results to the summary. Individual collections define what content to include in the summary | [optional] [default to True]

### Return type

[**Issuer**](Issuer.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Issuer was updated |  -  |
**404** | Issuer does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_policy**
> Policy replace_policy(policy_id, policy)

Update a policy

Update a policy

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
    api_instance = agilicus_api.IssuersApi(api_client)
    policy_id = '1234' # str | Policy Unique identifier
policy = agilicus_api.Policy() # Policy | Policy

    try:
        # Update a policy
        api_response = api_instance.replace_policy(policy_id, policy)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->replace_policy: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **policy_id** | **str**| Policy Unique identifier | 
 **policy** | [**Policy**](Policy.md)| Policy | 

### Return type

[**Policy**](Policy.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Policy was updated |  -  |
**400** | The request was invalid. |  -  |
**404** | Policy does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_policy_rule**
> PolicyRule replace_policy_rule(policy_id, policy_rule_id, policy_rule)

Update a policy rule

Update a policy rule

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
    api_instance = agilicus_api.IssuersApi(api_client)
    policy_id = '1234' # str | Policy Unique identifier
policy_rule_id = '1234' # str | Policy Rule Unique identifier
policy_rule = agilicus_api.PolicyRule() # PolicyRule | Policy Rule

    try:
        # Update a policy rule
        api_response = api_instance.replace_policy_rule(policy_id, policy_rule_id, policy_rule)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->replace_policy_rule: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **policy_id** | **str**| Policy Unique identifier | 
 **policy_rule_id** | **str**| Policy Rule Unique identifier | 
 **policy_rule** | [**PolicyRule**](PolicyRule.md)| Policy Rule | 

### Return type

[**PolicyRule**](PolicyRule.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Policy Rule was updated |  -  |
**404** | Policy Rule does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_root**
> Issuer replace_root(issuer_id, issuer, summarize_collection=summarize_collection)

Update an issuer

Update an issuer

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
    api_instance = agilicus_api.IssuersApi(api_client)
    issuer_id = '1234' # str | issuer_id path
issuer = agilicus_api.Issuer() # Issuer | Issuer
summarize_collection = True # bool | Restrict the results to the summary. Individual collections define what content to include in the summary (optional) (default to True)

    try:
        # Update an issuer
        api_response = api_instance.replace_root(issuer_id, issuer, summarize_collection=summarize_collection)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->replace_root: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issuer_id** | **str**| issuer_id path | 
 **issuer** | [**Issuer**](Issuer.md)| Issuer | 
 **summarize_collection** | **bool**| Restrict the results to the summary. Individual collections define what content to include in the summary | [optional] [default to True]

### Return type

[**Issuer**](Issuer.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Issuer was updated |  -  |
**404** | Issuer does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **reset_to_default_policy**
> Policy reset_to_default_policy(issuer_id, reset_policy_request)

Reset the current policy to the default policy

Reset the current policy to the default policy. This will create a new policy as the active policy for your organisation. The old policy will still exist with the same policy_id but will be disassociated with this issuer. 

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
    api_instance = agilicus_api.IssuersApi(api_client)
    issuer_id = '1234' # str | issuer_id path
reset_policy_request = agilicus_api.ResetPolicyRequest() # ResetPolicyRequest | Policy

    try:
        # Reset the current policy to the default policy
        api_response = api_instance.reset_to_default_policy(issuer_id, reset_policy_request)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling IssuersApi->reset_to_default_policy: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issuer_id** | **str**| issuer_id path | 
 **reset_policy_request** | [**ResetPolicyRequest**](ResetPolicyRequest.md)| Policy | 

### Return type

[**Policy**](Policy.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully reset the policy to the default. The new policy for your organisation is returned in the response |  -  |
**400** | An invalid request to reset the policy |  -  |
**404** | A policy does not exist matching that policy_id and org_id |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

