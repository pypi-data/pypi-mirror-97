# agilicus_api.CertificatesApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_cert**](CertificatesApi.md#create_cert) | **POST** /v1/certificates | Creates a X509Certificate
[**delete_agent_csr**](CertificatesApi.md#delete_agent_csr) | **DELETE** /v1/agent_connectors/{connector_id}/certificate_signing_requests/{csr_id} | Delete a CertSigningReq
[**delete_cert**](CertificatesApi.md#delete_cert) | **DELETE** /v1/certificates/{certificate_id} | Delete a X509Certificate
[**delete_csr**](CertificatesApi.md#delete_csr) | **DELETE** /v1/certificate_signing_requests/{csr_id} | Delete a CertSigningReq
[**get_cert**](CertificatesApi.md#get_cert) | **GET** /v1/certificates/{certificate_id} | Get a X509Certificate
[**get_csr**](CertificatesApi.md#get_csr) | **GET** /v1/certificate_signing_requests/{csr_id} | Get a CertSigningReq
[**list_certs**](CertificatesApi.md#list_certs) | **GET** /v1/certificates | list certificates
[**list_csr**](CertificatesApi.md#list_csr) | **GET** /v1/certificate_signing_requests | list certificate signing requests
[**replace_csr**](CertificatesApi.md#replace_csr) | **PUT** /v1/certificate_signing_requests/{csr_id} | Update a CertSigningReq


# **create_cert**
> X509Certificate create_cert(x509_certificate)

Creates a X509Certificate

Creates a X509Certificate 

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
    api_instance = agilicus_api.CertificatesApi(api_client)
    x509_certificate = agilicus_api.X509Certificate() # X509Certificate | 

    try:
        # Creates a X509Certificate
        api_response = api_instance.create_cert(x509_certificate)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling CertificatesApi->create_cert: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x509_certificate** | [**X509Certificate**](X509Certificate.md)|  | 

### Return type

[**X509Certificate**](X509Certificate.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | X509Certificate created and returned. |  -  |
**404** | CertSigningReq does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_agent_csr**
> delete_agent_csr(connector_id, csr_id, org_id=org_id)

Delete a CertSigningReq

Delete a CertSigningReq

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
    api_instance = agilicus_api.CertificatesApi(api_client)
    connector_id = '1234' # str | connector id path
csr_id = '1234' # str | A certificate signing request id
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Delete a CertSigningReq
        api_instance.delete_agent_csr(connector_id, csr_id, org_id=org_id)
    except ApiException as e:
        print("Exception when calling CertificatesApi->delete_agent_csr: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connector_id** | **str**| connector id path | 
 **csr_id** | **str**| A certificate signing request id | 
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
**204** | CertSigningReq was deleted |  -  |
**404** | CertSigningReq does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_cert**
> delete_cert(certificate_id, org_id=org_id)

Delete a X509Certificate

Delete a X509Certificate

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
    api_instance = agilicus_api.CertificatesApi(api_client)
    certificate_id = '1234' # str | A certificate id
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Delete a X509Certificate
        api_instance.delete_cert(certificate_id, org_id=org_id)
    except ApiException as e:
        print("Exception when calling CertificatesApi->delete_cert: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **certificate_id** | **str**| A certificate id | 
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
**204** | X509Certificate was deleted |  -  |
**404** | X509Certificate does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_csr**
> delete_csr(csr_id, org_id=org_id)

Delete a CertSigningReq

Delete a CertSigningReq

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
    api_instance = agilicus_api.CertificatesApi(api_client)
    csr_id = '1234' # str | A certificate signing request id
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Delete a CertSigningReq
        api_instance.delete_csr(csr_id, org_id=org_id)
    except ApiException as e:
        print("Exception when calling CertificatesApi->delete_csr: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **csr_id** | **str**| A certificate signing request id | 
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
**204** | CertSigningReq was deleted |  -  |
**404** | CertSigningReq does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_cert**
> X509Certificate get_cert(certificate_id, org_id=org_id)

Get a X509Certificate

Get a X509Certificate

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
    api_instance = agilicus_api.CertificatesApi(api_client)
    certificate_id = '1234' # str | A certificate id
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Get a X509Certificate
        api_response = api_instance.get_cert(certificate_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling CertificatesApi->get_cert: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **certificate_id** | **str**| A certificate id | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**X509Certificate**](X509Certificate.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | X509Certificate found and returned |  -  |
**404** | X509Certificate does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_csr**
> CertSigningReq get_csr(csr_id, org_id=org_id)

Get a CertSigningReq

Get a CertSigningReq

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
    api_instance = agilicus_api.CertificatesApi(api_client)
    csr_id = '1234' # str | A certificate signing request id
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Get a CertSigningReq
        api_response = api_instance.get_csr(csr_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling CertificatesApi->get_csr: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
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
**404** | CertSigningReq does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_certs**
> ListX509CertificateResponse list_certs(limit=limit, org_id=org_id)

list certificates

List certificates 

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
    api_instance = agilicus_api.CertificatesApi(api_client)
    limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # list certificates
        api_response = api_instance.list_certs(limit=limit, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling CertificatesApi->list_certs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**ListX509CertificateResponse**](ListX509CertificateResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return a list of X509Certificate |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_csr**
> ListCertSigningReqResponse list_csr(limit=limit, org_id=org_id, reason=reason, not_valid_after=not_valid_after)

list certificate signing requests

List certificate signing requests. 

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
    api_instance = agilicus_api.CertificatesApi(api_client)
    limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
org_id = '1234' # str | Organisation Unique identifier (optional)
reason = agilicus_api.CSRReasonEnum() # CSRReasonEnum | Query a CSR based on its reason status (optional)
not_valid_after = 'in 30 days' # str | Search criteria for finding expired certificates * In UTC. * Supports human-friendly values. * Example, find all expired certificates in 30 days: not_after_after=\"in 30 days\" * Example, find all expired certificates today:  not_valid_after=\"tomorrow\" * Example, find all expired now:  not_valid_after=\"now\"  (optional)

    try:
        # list certificate signing requests
        api_response = api_instance.list_csr(limit=limit, org_id=org_id, reason=reason, not_valid_after=not_valid_after)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling CertificatesApi->list_csr: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **reason** | [**CSRReasonEnum**](.md)| Query a CSR based on its reason status | [optional] 
 **not_valid_after** | **str**| Search criteria for finding expired certificates * In UTC. * Supports human-friendly values. * Example, find all expired certificates in 30 days: not_after_after&#x3D;\&quot;in 30 days\&quot; * Example, find all expired certificates today:  not_valid_after&#x3D;\&quot;tomorrow\&quot; * Example, find all expired now:  not_valid_after&#x3D;\&quot;now\&quot;  | [optional] 

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

# **replace_csr**
> CertSigningReq replace_csr(csr_id, org_id=org_id, cert_signing_req=cert_signing_req)

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
    api_instance = agilicus_api.CertificatesApi(api_client)
    csr_id = '1234' # str | A certificate signing request id
org_id = '1234' # str | Organisation Unique identifier (optional)
cert_signing_req = agilicus_api.CertSigningReq() # CertSigningReq |  (optional)

    try:
        # Update a CertSigningReq
        api_response = api_instance.replace_csr(csr_id, org_id=org_id, cert_signing_req=cert_signing_req)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling CertificatesApi->replace_csr: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
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
**404** | csr does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

