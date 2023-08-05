# agilicus_api.TokensApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_api_key**](TokensApi.md#create_api_key) | **POST** /v1/api_keys | Create an API Key
[**create_api_key_introspection**](TokensApi.md#create_api_key_introspection) | **POST** /v1/api_keys/introspect | Introspect an API Key
[**create_authentication_document**](TokensApi.md#create_authentication_document) | **POST** /v1/authentication_documents | Create a authentication document
[**create_bulk_revoke_token_task**](TokensApi.md#create_bulk_revoke_token_task) | **POST** /v1/tokens/bulk_revoke | Revoke a set of tokens
[**create_introspect_token**](TokensApi.md#create_introspect_token) | **POST** /v1/tokens/introspect | Introspect a token
[**create_introspect_token_all_sub_orgs**](TokensApi.md#create_introspect_token_all_sub_orgs) | **POST** /v1/tokens/introspect_all_sub_orgs | Introspect a token in all sub orgs
[**create_reissued_token**](TokensApi.md#create_reissued_token) | **POST** /v1/tokens/reissue | Issue a new token from another
[**create_revoke_token_task**](TokensApi.md#create_revoke_token_task) | **POST** /v1/tokens/revoke | Revoke a token
[**create_token**](TokensApi.md#create_token) | **POST** /v1/tokens | Create a token
[**create_token_validation**](TokensApi.md#create_token_validation) | **POST** /v1/tokens/validations | Validate a token request
[**delete_api_key**](TokensApi.md#delete_api_key) | **DELETE** /v1/api_keys/{api_key_id} | Delete an API Key
[**delete_authentication_document**](TokensApi.md#delete_authentication_document) | **DELETE** /v1/authentication_documents/{document_id} | Delete a authentication document
[**get_api_key**](TokensApi.md#get_api_key) | **GET** /v1/api_keys/{api_key_id} | Get an API Key
[**get_authentication_document**](TokensApi.md#get_authentication_document) | **GET** /v1/authentication_documents/{document_id} | Get a authentication document
[**list_api_keys**](TokensApi.md#list_api_keys) | **GET** /v1/api_keys | List API Keys
[**list_authentication_documents**](TokensApi.md#list_authentication_documents) | **GET** /v1/authentication_documents | List authentication documents
[**list_tokens**](TokensApi.md#list_tokens) | **GET** /v1/tokens | Query tokens
[**validate_identity_assertion**](TokensApi.md#validate_identity_assertion) | **POST** /v1/authentication_documents_rpc/validate_identity_assertion | Validate an identity assertion


# **create_api_key**
> APIKey create_api_key(api_key)

Create an API Key

Creates an API Key with the provided body. Note that the secret which serves as the key to provide access is only available when the API Key is created. 

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
    api_instance = agilicus_api.TokensApi(api_client)
    api_key = agilicus_api.APIKey() # APIKey | 

    try:
        # Create an API Key
        api_response = api_instance.create_api_key(api_key)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TokensApi->create_api_key: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_key** | [**APIKey**](APIKey.md)|  | 

### Return type

[**APIKey**](APIKey.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New API Key |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_api_key_introspection**
> APIKeyIntrospectResponse create_api_key_introspection(api_key_introspect)

Introspect an API Key

Introspect an API Key to determine its permissions

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
    api_instance = agilicus_api.TokensApi(api_client)
    api_key_introspect = agilicus_api.APIKeyIntrospect() # APIKeyIntrospect | API Key to introspect

    try:
        # Introspect an API Key
        api_response = api_instance.create_api_key_introspection(api_key_introspect)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TokensApi->create_api_key_introspection: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_key_introspect** | [**APIKeyIntrospect**](APIKeyIntrospect.md)| API Key to introspect | 

### Return type

[**APIKeyIntrospectResponse**](APIKeyIntrospectResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Introspection succeeded. |  -  |
**410** | The API Key has been revoked. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_authentication_document**
> AuthenticationDocument create_authentication_document(authentication_document)

Create a authentication document

Creates an authentication document with the provided body

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
    api_instance = agilicus_api.TokensApi(api_client)
    authentication_document = agilicus_api.AuthenticationDocument() # AuthenticationDocument | 

    try:
        # Create a authentication document
        api_response = api_instance.create_authentication_document(authentication_document)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TokensApi->create_authentication_document: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **authentication_document** | [**AuthenticationDocument**](AuthenticationDocument.md)|  | 

### Return type

[**AuthenticationDocument**](AuthenticationDocument.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New authentication document |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_bulk_revoke_token_task**
> BulkTokenRevokeResponse create_bulk_revoke_token_task(bulk_token_revoke)

Revoke a set of tokens

Revoke a set of tokens. The body parameters determine the set of tokens

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
    api_instance = agilicus_api.TokensApi(api_client)
    bulk_token_revoke = agilicus_api.BulkTokenRevoke() # BulkTokenRevoke | Token to revoke

    try:
        # Revoke a set of tokens
        api_response = api_instance.create_bulk_revoke_token_task(bulk_token_revoke)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TokensApi->create_bulk_revoke_token_task: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **bulk_token_revoke** | [**BulkTokenRevoke**](BulkTokenRevoke.md)| Token to revoke | 

### Return type

[**BulkTokenRevokeResponse**](BulkTokenRevokeResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | tokens have been revoked |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_introspect_token**
> Token create_introspect_token(token_introspect)

Introspect a token

Introspect a token

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
    api_instance = agilicus_api.TokensApi(api_client)
    token_introspect = agilicus_api.TokenIntrospect() # TokenIntrospect | Token to introspect

    try:
        # Introspect a token
        api_response = api_instance.create_introspect_token(token_introspect)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TokensApi->create_introspect_token: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **token_introspect** | [**TokenIntrospect**](TokenIntrospect.md)| Token to introspect | 

### Return type

[**Token**](Token.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Traffic token |  -  |
**410** | Token has been revoked |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_introspect_token_all_sub_orgs**
> ManyOrgTokenIntrospectResponse create_introspect_token_all_sub_orgs(token_introspect)

Introspect a token in all sub orgs

Introspect a token in all sub orgs

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
    api_instance = agilicus_api.TokensApi(api_client)
    token_introspect = agilicus_api.TokenIntrospect() # TokenIntrospect | Token to introspect

    try:
        # Introspect a token in all sub orgs
        api_response = api_instance.create_introspect_token_all_sub_orgs(token_introspect)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TokensApi->create_introspect_token_all_sub_orgs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **token_introspect** | [**TokenIntrospect**](TokenIntrospect.md)| Token to introspect | 

### Return type

[**ManyOrgTokenIntrospectResponse**](ManyOrgTokenIntrospectResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Traffic token |  -  |
**410** | Token has been revoked |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_reissued_token**
> RawToken create_reissued_token(token_reissue_request)

Issue a new token from another

Issues a new token with the same or reduced scope to the one presented. Use this to retrieve a token for accessing a different organisation than the one you're currently operating on. Note that the presented token remains valid if it already was. If it is not valid, or the you do not have permissions in the requested organisation, the request will fail. The token will expire at the same time as the presented token. 

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
    api_instance = agilicus_api.TokensApi(api_client)
    token_reissue_request = agilicus_api.TokenReissueRequest() # TokenReissueRequest | The token request

    try:
        # Issue a new token from another
        api_response = api_instance.create_reissued_token(token_reissue_request)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TokensApi->create_reissued_token: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **token_reissue_request** | [**TokenReissueRequest**](TokenReissueRequest.md)| The token request | 

### Return type

[**RawToken**](RawToken.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The token was succesfully issued. It is contained in the response.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_revoke_token_task**
> create_revoke_token_task(token_revoke)

Revoke a token

Revoke a token

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
    api_instance = agilicus_api.TokensApi(api_client)
    token_revoke = agilicus_api.TokenRevoke() # TokenRevoke | Token to revoke

    try:
        # Revoke a token
        api_instance.create_revoke_token_task(token_revoke)
    except ApiException as e:
        print("Exception when calling TokensApi->create_revoke_token_task: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **token_revoke** | [**TokenRevoke**](TokenRevoke.md)| Token to revoke | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | token has been revoked |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_token**
> RawToken create_token(create_token_request)

Create a token

Create a token

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
    api_instance = agilicus_api.TokensApi(api_client)
    create_token_request = agilicus_api.CreateTokenRequest() # CreateTokenRequest | Rule to sign

    try:
        # Create a token
        api_response = api_instance.create_token(create_token_request)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TokensApi->create_token: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_token_request** | [**CreateTokenRequest**](CreateTokenRequest.md)| Rule to sign | 

### Return type

[**RawToken**](RawToken.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully signed assertion |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_token_validation**
> CreateTokenRequest create_token_validation(create_token_request)

Validate a token request

Validate a token request prior to creating a token. This verifies the user has permission to access the scopes requested

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
    api_instance = agilicus_api.TokensApi(api_client)
    create_token_request = agilicus_api.CreateTokenRequest() # CreateTokenRequest | Token to validate

    try:
        # Validate a token request
        api_response = api_instance.create_token_validation(create_token_request)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TokensApi->create_token_validation: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_token_request** | [**CreateTokenRequest**](CreateTokenRequest.md)| Token to validate | 

### Return type

[**CreateTokenRequest**](CreateTokenRequest.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully validated token request. The user has permission to access specified scopes |  -  |
**403** | Token request is invalid |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_api_key**
> delete_api_key(api_key_id, user_id=user_id, org_id=org_id)

Delete an API Key

Deletes the requested API Key

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
    api_instance = agilicus_api.TokensApi(api_client)
    api_key_id = '1234' # str | An API Key ID found in a path
user_id = '1234' # str | Query based on user id (optional)
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Delete an API Key
        api_instance.delete_api_key(api_key_id, user_id=user_id, org_id=org_id)
    except ApiException as e:
        print("Exception when calling TokensApi->delete_api_key: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_key_id** | **str**| An API Key ID found in a path | 
 **user_id** | **str**| Query based on user id | [optional] 
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
**204** | API Key was deleted |  -  |
**404** | API Key does not exist. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_authentication_document**
> delete_authentication_document(document_id, user_id=user_id, org_id=org_id)

Delete a authentication document

Deletes the requested authentication document

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
    api_instance = agilicus_api.TokensApi(api_client)
    document_id = '1234' # str | Authetication document path
user_id = '1234' # str | Query based on user id (optional)
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Delete a authentication document
        api_instance.delete_authentication_document(document_id, user_id=user_id, org_id=org_id)
    except ApiException as e:
        print("Exception when calling TokensApi->delete_authentication_document: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **document_id** | **str**| Authetication document path | 
 **user_id** | **str**| Query based on user id | [optional] 
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
**204** | authentication document was deleted |  -  |
**404** | authentication document does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_api_key**
> APIKey get_api_key(api_key_id, user_id=user_id, org_id=org_id)

Get an API Key

Gets the requested API Key

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
    api_instance = agilicus_api.TokensApi(api_client)
    api_key_id = '1234' # str | An API Key ID found in a path
user_id = '1234' # str | Query based on user id (optional)
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Get an API Key
        api_response = api_instance.get_api_key(api_key_id, user_id=user_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TokensApi->get_api_key: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_key_id** | **str**| An API Key ID found in a path | 
 **user_id** | **str**| Query based on user id | [optional] 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**APIKey**](APIKey.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | API Key found and returned |  -  |
**404** | API Key does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_authentication_document**
> AuthenticationDocument get_authentication_document(document_id, user_id=user_id, org_id=org_id)

Get a authentication document

Gets the requested authentication document

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
    api_instance = agilicus_api.TokensApi(api_client)
    document_id = '1234' # str | Authetication document path
user_id = '1234' # str | Query based on user id (optional)
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Get a authentication document
        api_response = api_instance.get_authentication_document(document_id, user_id=user_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TokensApi->get_authentication_document: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **document_id** | **str**| Authetication document path | 
 **user_id** | **str**| Query based on user id | [optional] 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**AuthenticationDocument**](AuthenticationDocument.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | authentication document found and returned |  -  |
**404** | authentication document does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_api_keys**
> ListAPIKeysResponse list_api_keys(limit=limit, user_id=user_id, org_id=org_id)

List API Keys

Lists API Keys according to query parameters

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
    api_instance = agilicus_api.TokensApi(api_client)
    limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
user_id = '1234' # str | Query based on user id (optional)
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # List API Keys
        api_response = api_instance.list_api_keys(limit=limit, user_id=user_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TokensApi->list_api_keys: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **user_id** | **str**| Query based on user id | [optional] 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**ListAPIKeysResponse**](ListAPIKeysResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return a list of API Keys |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_authentication_documents**
> ListAuthenticationDocumentResponse list_authentication_documents(limit=limit, user_id=user_id, org_id=org_id)

List authentication documents

Lists authentication documents according to query parameters

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
    api_instance = agilicus_api.TokensApi(api_client)
    limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
user_id = '1234' # str | Query based on user id (optional)
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # List authentication documents
        api_response = api_instance.list_authentication_documents(limit=limit, user_id=user_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TokensApi->list_authentication_documents: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **user_id** | **str**| Query based on user id | [optional] 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**ListAuthenticationDocumentResponse**](ListAuthenticationDocumentResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return a list of authentication documents |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_tokens**
> ListTokensResponse list_tokens(limit=limit, sub=sub, exp_from=exp_from, exp_to=exp_to, iat_from=iat_from, iat_to=iat_to, jti=jti, org=org, revoked=revoked, session=session)

Query tokens

Query tokens

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
    api_instance = agilicus_api.TokensApi(api_client)
    limit = 100 # int | limit the number of rows in the response (optional) (default to 100)
sub = 'sub_example' # str | search criteria sub (optional)
exp_from = 'exp_from_example' # str | search criteria expired from using dateparser (optional)
exp_to = 'exp_to_example' # str | search criteria expired to using dateparser (optional)
iat_from = 'iat_from_example' # str | search criteria issued from using dateparser (optional)
iat_to = 'iat_to_example' # str | search criteria issued to using dateparser (optional)
jti = 'jti_example' # str | search criteria using jti (optional)
org = 'org_example' # str | search criteria using org (optional)
revoked = True # bool | search criteria for revoked tokens (optional)
session = 'session_example' # str | search criteria using session (optional)

    try:
        # Query tokens
        api_response = api_instance.list_tokens(limit=limit, sub=sub, exp_from=exp_from, exp_to=exp_to, iat_from=iat_from, iat_to=iat_to, jti=jti, org=org, revoked=revoked, session=session)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TokensApi->list_tokens: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 100]
 **sub** | **str**| search criteria sub | [optional] 
 **exp_from** | **str**| search criteria expired from using dateparser | [optional] 
 **exp_to** | **str**| search criteria expired to using dateparser | [optional] 
 **iat_from** | **str**| search criteria issued from using dateparser | [optional] 
 **iat_to** | **str**| search criteria issued to using dateparser | [optional] 
 **jti** | **str**| search criteria using jti | [optional] 
 **org** | **str**| search criteria using org | [optional] 
 **revoked** | **bool**| search criteria for revoked tokens | [optional] 
 **session** | **str**| search criteria using session | [optional] 

### Return type

[**ListTokensResponse**](ListTokensResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return traffic tokens list |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **validate_identity_assertion**
> IdentityAssertionResponse validate_identity_assertion(identity_assertion)

Validate an identity assertion

Validate an identity assertion to asscertain if the request for a token is valid

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
    api_instance = agilicus_api.TokensApi(api_client)
    identity_assertion = agilicus_api.IdentityAssertion() # IdentityAssertion | Token to validate

    try:
        # Validate an identity assertion
        api_response = api_instance.validate_identity_assertion(identity_assertion)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TokensApi->validate_identity_assertion: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identity_assertion** | [**IdentityAssertion**](IdentityAssertion.md)| Token to validate | 

### Return type

[**IdentityAssertionResponse**](IdentityAssertionResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully validated the identity assertion |  -  |
**400** | The identity assertion is invalid. This can be for a number of reasons. Including an invalid identifier, invalid signature, or invalid contents. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

