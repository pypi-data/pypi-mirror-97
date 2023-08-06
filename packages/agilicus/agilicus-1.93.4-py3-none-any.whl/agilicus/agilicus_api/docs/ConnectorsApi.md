# agilicus_api.ConnectorsApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_agent_connector**](ConnectorsApi.md#create_agent_connector) | **POST** /v1/agent_connectors | Create an agent connector
[**create_agent_csr**](ConnectorsApi.md#create_agent_csr) | **POST** /v1/agent_connectors/{connector_id}/certificate_signing_requests | Creates a CertSigningReq
[**create_agent_stats**](ConnectorsApi.md#create_agent_stats) | **POST** /v1/agent_connectors/{connector_id}/stats | Creates an AgentConnectorStats record.
[**create_csr**](ConnectorsApi.md#create_csr) | **POST** /v1/certificate_signing_requests | Creates a CertSigningReq
[**create_ipsec_connector**](ConnectorsApi.md#create_ipsec_connector) | **POST** /v1/ipsec_connectors | Create an IPsec connector
[**delete_agent_connector**](ConnectorsApi.md#delete_agent_connector) | **DELETE** /v1/agent_connectors/{connector_id} | Delete a agent
[**delete_connector**](ConnectorsApi.md#delete_connector) | **DELETE** /v1/connectors/{connector_id} | Delete a connector
[**delete_ipsec_connector**](ConnectorsApi.md#delete_ipsec_connector) | **DELETE** /v1/ipsec_connectors/{connector_id} | Delete an IPsec connector
[**get_agent_connector**](ConnectorsApi.md#get_agent_connector) | **GET** /v1/agent_connectors/{connector_id} | Get an agent
[**get_agent_csr**](ConnectorsApi.md#get_agent_csr) | **GET** /v1/agent_connectors/{connector_id}/certificate_signing_requests/{csr_id} | Update a CertSigningReq
[**get_agent_info**](ConnectorsApi.md#get_agent_info) | **GET** /v1/agent_connectors/{connector_id}/info | Get information associated with connector
[**get_agent_stats**](ConnectorsApi.md#get_agent_stats) | **GET** /v1/agent_connectors/{connector_id}/stats | Get the AgentConnector stats
[**get_connector**](ConnectorsApi.md#get_connector) | **GET** /v1/connectors/{connector_id} | Get a connector
[**get_ipsec_connector**](ConnectorsApi.md#get_ipsec_connector) | **GET** /v1/ipsec_connectors/{connector_id} | Get an IPsec connector
[**get_ipsec_connector_info**](ConnectorsApi.md#get_ipsec_connector_info) | **GET** /v1/ipsec_connectors/{connector_id}/info | Get IPsec connector runtime information
[**list_agent_connector**](ConnectorsApi.md#list_agent_connector) | **GET** /v1/agent_connectors | list agent connectors
[**list_agent_csr**](ConnectorsApi.md#list_agent_csr) | **GET** /v1/agent_connectors/{connector_id}/certificate_signing_requests | list agent connector certificate signing requests
[**list_connector**](ConnectorsApi.md#list_connector) | **GET** /v1/connectors | List connectors
[**list_ipsec_connector**](ConnectorsApi.md#list_ipsec_connector) | **GET** /v1/ipsec_connectors | list IPsec connectors
[**replace_agent_connector**](ConnectorsApi.md#replace_agent_connector) | **PUT** /v1/agent_connectors/{connector_id} | Update an agent
[**replace_agent_csr**](ConnectorsApi.md#replace_agent_csr) | **PUT** /v1/agent_connectors/{connector_id}/certificate_signing_requests/{csr_id} | Update a CertSigningReq
[**replace_ipsec_connector**](ConnectorsApi.md#replace_ipsec_connector) | **PUT** /v1/ipsec_connectors/{connector_id} | Update an IPsec connector


# **create_agent_connector**
> AgentConnector create_agent_connector(agent_connector)

Create an agent connector

Create an agent connector

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
    api_instance = agilicus_api.ConnectorsApi(api_client)
    agent_connector = agilicus_api.AgentConnector() # AgentConnector | 

    try:
        # Create an agent connector
        api_response = api_instance.create_agent_connector(agent_connector)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ConnectorsApi->create_agent_connector: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **agent_connector** | [**AgentConnector**](AgentConnector.md)|  | 

### Return type

[**AgentConnector**](AgentConnector.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New agent |  -  |
**400** | The contents of the request body are invalid |  -  |
**409** | agent already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_agent_csr**
> CertSigningReq create_agent_csr(connector_id, cert_signing_req)

Creates a CertSigningReq

Creates a CertSigningReq 

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
    api_instance = agilicus_api.ConnectorsApi(api_client)
    connector_id = '1234' # str | connector id path
cert_signing_req = agilicus_api.CertSigningReq() # CertSigningReq | 

    try:
        # Creates a CertSigningReq
        api_response = api_instance.create_agent_csr(connector_id, cert_signing_req)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ConnectorsApi->create_agent_csr: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path | 
 **cert_signing_req** | [**CertSigningReq**](CertSigningReq.md)|  | 

### Return type

[**CertSigningReq**](CertSigningReq.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | CertSigningReq created and returned. |  -  |
**404** | CertSigningReq does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_agent_stats**
> AgentConnectorStats create_agent_stats(connector_id, agent_connector_stats)

Creates an AgentConnectorStats record.

Publishes the most recent stats collected by the AgentConnector. Currently only the most recent AgentCollectorStats is retained, but in the future some history may be recorded. 

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
    api_instance = agilicus_api.ConnectorsApi(api_client)
    connector_id = '1234' # str | connector id path
agent_connector_stats = agilicus_api.AgentConnectorStats() # AgentConnectorStats | 

    try:
        # Creates an AgentConnectorStats record.
        api_response = api_instance.create_agent_stats(connector_id, agent_connector_stats)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ConnectorsApi->create_agent_stats: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path | 
 **agent_connector_stats** | [**AgentConnectorStats**](AgentConnectorStats.md)|  | 

### Return type

[**AgentConnectorStats**](AgentConnectorStats.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | AgentConnectorStats created and returned. |  -  |
**404** | AgentConnector does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_csr**
> CertSigningReq create_csr(cert_signing_req)

Creates a CertSigningReq

Creates a CertSigningReq 

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
    api_instance = agilicus_api.ConnectorsApi(api_client)
    cert_signing_req = agilicus_api.CertSigningReq() # CertSigningReq | 

    try:
        # Creates a CertSigningReq
        api_response = api_instance.create_csr(cert_signing_req)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ConnectorsApi->create_csr: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cert_signing_req** | [**CertSigningReq**](CertSigningReq.md)|  | 

### Return type

[**CertSigningReq**](CertSigningReq.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | CertSigningReq created and returned. |  -  |
**404** | CertSigningReq does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_ipsec_connector**
> IpsecConnector create_ipsec_connector(ipsec_connector)

Create an IPsec connector

Create an IPsec connector

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
    api_instance = agilicus_api.ConnectorsApi(api_client)
    ipsec_connector = agilicus_api.IpsecConnector() # IpsecConnector | 

    try:
        # Create an IPsec connector
        api_response = api_instance.create_ipsec_connector(ipsec_connector)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ConnectorsApi->create_ipsec_connector: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ipsec_connector** | [**IpsecConnector**](IpsecConnector.md)|  | 

### Return type

[**IpsecConnector**](IpsecConnector.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New IPsec connector |  -  |
**400** | The contents of the request body are invalid |  -  |
**409** | IPsec connector already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_agent_connector**
> delete_agent_connector(connector_id, org_id=org_id)

Delete a agent

Delete a agent

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
    api_instance = agilicus_api.ConnectorsApi(api_client)
    connector_id = '1234' # str | connector id path
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Delete a agent
        api_instance.delete_agent_connector(connector_id, org_id=org_id)
    except ApiException as e:
        print("Exception when calling ConnectorsApi->delete_agent_connector: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path | 
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
**204** | agent was deleted |  -  |
**404** | agent does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_connector**
> delete_connector(connector_id, org_id=org_id)

Delete a connector

Delete a connector

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
    api_instance = agilicus_api.ConnectorsApi(api_client)
    connector_id = '1234' # str | connector id path
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Delete a connector
        api_instance.delete_connector(connector_id, org_id=org_id)
    except ApiException as e:
        print("Exception when calling ConnectorsApi->delete_connector: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path | 
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
**204** | connector was deleted |  -  |
**404** | connector does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_ipsec_connector**
> delete_ipsec_connector(connector_id, org_id=org_id)

Delete an IPsec connector

Delete an IPsec connector

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
    api_instance = agilicus_api.ConnectorsApi(api_client)
    connector_id = '1234' # str | connector id path
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Delete an IPsec connector
        api_instance.delete_ipsec_connector(connector_id, org_id=org_id)
    except ApiException as e:
        print("Exception when calling ConnectorsApi->delete_ipsec_connector: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path | 
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
**204** | IPsec connector was deleted |  -  |
**404** | IPsec connector does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_agent_connector**
> AgentConnector get_agent_connector(connector_id, org_id=org_id)

Get an agent

Get an agent

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
    api_instance = agilicus_api.ConnectorsApi(api_client)
    connector_id = '1234' # str | connector id path
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Get an agent
        api_response = api_instance.get_agent_connector(connector_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ConnectorsApi->get_agent_connector: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**AgentConnector**](AgentConnector.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | agent found and returned |  -  |
**404** | agent does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_agent_csr**
> CertSigningReq get_agent_csr(connector_id, csr_id, org_id=org_id)

Update a CertSigningReq

Update a CertSigningReq

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
    api_instance = agilicus_api.ConnectorsApi(api_client)
    connector_id = '1234' # str | connector id path
csr_id = '1234' # str | A certificate signing request id
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Update a CertSigningReq
        api_response = api_instance.get_agent_csr(connector_id, csr_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ConnectorsApi->get_agent_csr: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path | 
 **csr_id** | **str**| A certificate signing request id | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**CertSigningReq**](CertSigningReq.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | CertSigningReq found and returned |  -  |
**404** | CertSigningReq csr does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_agent_info**
> AgentConnectorInfo get_agent_info(connector_id, org_id=org_id)

Get information associated with connector

Get information associated with connector

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
    api_instance = agilicus_api.ConnectorsApi(api_client)
    connector_id = '1234' # str | connector id path
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Get information associated with connector
        api_response = api_instance.get_agent_info(connector_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ConnectorsApi->get_agent_info: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**AgentConnectorInfo**](AgentConnectorInfo.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | agent info found and returned |  -  |
**404** | agent does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_agent_stats**
> AgentConnectorStats get_agent_stats(connector_id, org_id=org_id)

Get the AgentConnector stats

Gets the most recent stats published by the AgentConnector

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
    api_instance = agilicus_api.ConnectorsApi(api_client)
    connector_id = '1234' # str | connector id path
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Get the AgentConnector stats
        api_response = api_instance.get_agent_stats(connector_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ConnectorsApi->get_agent_stats: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**AgentConnectorStats**](AgentConnectorStats.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | agent stats found and returned |  -  |
**404** | AgentConnector does not exist, or has not recently published any stats. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_connector**
> Connector get_connector(connector_id, org_id=org_id)

Get a connector

Get a connector

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
    api_instance = agilicus_api.ConnectorsApi(api_client)
    connector_id = '1234' # str | connector id path
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Get a connector
        api_response = api_instance.get_connector(connector_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ConnectorsApi->get_connector: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**Connector**](Connector.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | connector found and returned |  -  |
**404** | Connector does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_ipsec_connector**
> IpsecConnector get_ipsec_connector(connector_id, org_id=org_id)

Get an IPsec connector

Get an IPsec connector

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
    api_instance = agilicus_api.ConnectorsApi(api_client)
    connector_id = '1234' # str | connector id path
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Get an IPsec connector
        api_response = api_instance.get_ipsec_connector(connector_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ConnectorsApi->get_ipsec_connector: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**IpsecConnector**](IpsecConnector.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | IPsec connector found and returned |  -  |
**404** | IPsec connector does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_ipsec_connector_info**
> IpsecConnector get_ipsec_connector_info(connector_id, org_id=org_id)

Get IPsec connector runtime information

Get IPsec connector runtime information. 

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
    api_instance = agilicus_api.ConnectorsApi(api_client)
    connector_id = '1234' # str | connector id path
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Get IPsec connector runtime information
        api_response = api_instance.get_ipsec_connector_info(connector_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ConnectorsApi->get_ipsec_connector_info: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**IpsecConnector**](IpsecConnector.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | IPsec connector found and returned |  -  |
**404** | IPsec connector does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_agent_connector**
> ListAgentConnectorResponse list_agent_connector(limit=limit, org_id=org_id, name=name, show_stats=show_stats, page_at_id=page_at_id)

list agent connectors

list agent connectors. By default, an AgentConnector will not show stats when listed to speed up the query. Setting the show_stats parameter to true retrieve the stats for every AgentConnector. 

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
    api_instance = agilicus_api.ConnectorsApi(api_client)
    limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
org_id = '1234' # str | Organisation Unique identifier (optional)
name = 'host1_connector' # str | Query the connector by name (optional)
show_stats = False # bool | Whether the return value should include the stats for included objects. If false the query may run faster but will not include statistics. If not present, defaults to false.  (optional) (default to False)
page_at_id = 'foo@example.com' # str | Pagination based query with the id as the key. To get the initial entries supply an empty string. On subsequent requests, supply the `page_at_id` field from the list response.  (optional)

    try:
        # list agent connectors
        api_response = api_instance.list_agent_connector(limit=limit, org_id=org_id, name=name, show_stats=show_stats, page_at_id=page_at_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ConnectorsApi->list_agent_connector: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **name** | **str**| Query the connector by name | [optional] 
 **show_stats** | **bool**| Whether the return value should include the stats for included objects. If false the query may run faster but will not include statistics. If not present, defaults to false.  | [optional] [default to False]
 **page_at_id** | **str**| Pagination based query with the id as the key. To get the initial entries supply an empty string. On subsequent requests, supply the &#x60;page_at_id&#x60; field from the list response.  | [optional] 

### Return type

[**ListAgentConnectorResponse**](ListAgentConnectorResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return a list of agent connectors |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_agent_csr**
> ListCertSigningReqResponse list_agent_csr(connector_id, limit=limit, org_id=org_id, reason=reason)

list agent connector certificate signing requests

List agent connector certificate signing requests. 

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
    api_instance = agilicus_api.ConnectorsApi(api_client)
    connector_id = '1234' # str | connector id path
limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
org_id = '1234' # str | Organisation Unique identifier (optional)
reason = agilicus_api.CSRReasonEnum() # CSRReasonEnum | Query a CSR based on its reason status (optional)

    try:
        # list agent connector certificate signing requests
        api_response = api_instance.list_agent_csr(connector_id, limit=limit, org_id=org_id, reason=reason)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ConnectorsApi->list_agent_csr: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path | 
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **reason** | [**CSRReasonEnum**](.md)| Query a CSR based on its reason status | [optional] 

### Return type

[**ListCertSigningReqResponse**](ListCertSigningReqResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return a list of CertSigningReq |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_connector**
> ListConnectorResponse list_connector(limit=limit, org_id=org_id, name=name, type=type, show_stats=show_stats)

List connectors

List connectors. By default, Connectors will not show stats when listed to speed up the query. Set the show_stats parameter to true to retrieve the stats for every Connector. 

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
    api_instance = agilicus_api.ConnectorsApi(api_client)
    limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
org_id = '1234' # str | Organisation Unique identifier (optional)
name = 'host1_connector' # str | Query the connector by name (optional)
type = 'agent' # str | connector type (optional)
show_stats = False # bool | Whether the return value should include the stats for included objects. If false the query may run faster but will not include statistics. If not present, defaults to false.  (optional) (default to False)

    try:
        # List connectors
        api_response = api_instance.list_connector(limit=limit, org_id=org_id, name=name, type=type, show_stats=show_stats)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ConnectorsApi->list_connector: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **name** | **str**| Query the connector by name | [optional] 
 **type** | **str**| connector type | [optional] 
 **show_stats** | **bool**| Whether the return value should include the stats for included objects. If false the query may run faster but will not include statistics. If not present, defaults to false.  | [optional] [default to False]

### Return type

[**ListConnectorResponse**](ListConnectorResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return a list of connectors |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_ipsec_connector**
> ListIpsecConnectorResponse list_ipsec_connector(limit=limit, org_id=org_id, name=name, render_inheritance=render_inheritance)

list IPsec connectors

list IPsec connectors. 

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
    api_instance = agilicus_api.ConnectorsApi(api_client)
    limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
org_id = '1234' # str | Organisation Unique identifier (optional)
name = 'host1_connector' # str | Query the connector by name (optional)
render_inheritance = False # bool | Returns connections with their spec inherited as per their inherited_from property  (optional) (default to False)

    try:
        # list IPsec connectors
        api_response = api_instance.list_ipsec_connector(limit=limit, org_id=org_id, name=name, render_inheritance=render_inheritance)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ConnectorsApi->list_ipsec_connector: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **name** | **str**| Query the connector by name | [optional] 
 **render_inheritance** | **bool**| Returns connections with their spec inherited as per their inherited_from property  | [optional] [default to False]

### Return type

[**ListIpsecConnectorResponse**](ListIpsecConnectorResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return a list of IPsec connectors |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_agent_connector**
> AgentConnector replace_agent_connector(connector_id, org_id=org_id, agent_connector=agent_connector)

Update an agent

Update an agent

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
    api_instance = agilicus_api.ConnectorsApi(api_client)
    connector_id = '1234' # str | connector id path
org_id = '1234' # str | Organisation Unique identifier (optional)
agent_connector = agilicus_api.AgentConnector() # AgentConnector |  (optional)

    try:
        # Update an agent
        api_response = api_instance.replace_agent_connector(connector_id, org_id=org_id, agent_connector=agent_connector)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ConnectorsApi->replace_agent_connector: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **agent_connector** | [**AgentConnector**](AgentConnector.md)|  | [optional] 

### Return type

[**AgentConnector**](AgentConnector.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | agent updated |  -  |
**400** | The contents of the request body are invalid |  -  |
**404** | agent does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_agent_csr**
> CertSigningReq replace_agent_csr(connector_id, csr_id, org_id=org_id, cert_signing_req=cert_signing_req)

Update a CertSigningReq

Update a CertSigningReq

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
    api_instance = agilicus_api.ConnectorsApi(api_client)
    connector_id = '1234' # str | connector id path
csr_id = '1234' # str | A certificate signing request id
org_id = '1234' # str | Organisation Unique identifier (optional)
cert_signing_req = agilicus_api.CertSigningReq() # CertSigningReq |  (optional)

    try:
        # Update a CertSigningReq
        api_response = api_instance.replace_agent_csr(connector_id, csr_id, org_id=org_id, cert_signing_req=cert_signing_req)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ConnectorsApi->replace_agent_csr: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path | 
 **csr_id** | **str**| A certificate signing request id | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **cert_signing_req** | [**CertSigningReq**](CertSigningReq.md)|  | [optional] 

### Return type

[**CertSigningReq**](CertSigningReq.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | CertSigningReq updated |  -  |
**400** | The contents of the request body are invalid |  -  |
**404** | CertSigningReq does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_ipsec_connector**
> IpsecConnector replace_ipsec_connector(connector_id, org_id=org_id, ipsec_connector=ipsec_connector)

Update an IPsec connector

Update an IPsec connector

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
    api_instance = agilicus_api.ConnectorsApi(api_client)
    connector_id = '1234' # str | connector id path
org_id = '1234' # str | Organisation Unique identifier (optional)
ipsec_connector = agilicus_api.IpsecConnector() # IpsecConnector |  (optional)

    try:
        # Update an IPsec connector
        api_response = api_instance.replace_ipsec_connector(connector_id, org_id=org_id, ipsec_connector=ipsec_connector)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ConnectorsApi->replace_ipsec_connector: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **ipsec_connector** | [**IpsecConnector**](IpsecConnector.md)|  | [optional] 

### Return type

[**IpsecConnector**](IpsecConnector.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | IPsec connector updated |  -  |
**400** | The contents of the request body are invalid |  -  |
**404** | agent does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

