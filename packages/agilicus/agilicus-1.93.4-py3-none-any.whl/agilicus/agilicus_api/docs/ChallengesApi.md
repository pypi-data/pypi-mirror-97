# agilicus_api.ChallengesApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_challenge**](ChallengesApi.md#create_challenge) | **POST** /v1/challenges | create a challenge
[**create_totp_enrollment**](ChallengesApi.md#create_totp_enrollment) | **POST** /v1/challenge_enrollment/totp | create a TOTP challenge enrollment
[**create_webauthn_enrollment**](ChallengesApi.md#create_webauthn_enrollment) | **POST** /v1/challenge_enrollment/webauthn | create a WebAuthN challenge enrollment
[**delete_challenge**](ChallengesApi.md#delete_challenge) | **DELETE** /v1/challenges/{challenge_id} | Delete the challenge specified by challenge_id
[**delete_totp_enrollment**](ChallengesApi.md#delete_totp_enrollment) | **DELETE** /v1/challenge_enrollment/totp/{totp_id} | Delete the TOTP enrollment specified by totp id
[**delete_webauthn_enrollment**](ChallengesApi.md#delete_webauthn_enrollment) | **DELETE** /v1/challenge_enrollment/webauthn/{webauthn_id} | Delete the WebAuthN enrollment specified by webauthn_id
[**get_answer**](ChallengesApi.md#get_answer) | **GET** /v1/challenges/{challenge_id}/answers | answer a challenge
[**get_challenge**](ChallengesApi.md#get_challenge) | **GET** /v1/challenges/{challenge_id} | Get the challenge specified by challenge_id
[**get_totp_enrollment**](ChallengesApi.md#get_totp_enrollment) | **GET** /v1/challenge_enrollment/totp/{totp_id} | Get the TOTP enrollment specified by totp_id
[**get_webauthn_enrollment**](ChallengesApi.md#get_webauthn_enrollment) | **GET** /v1/challenge_enrollment/webauthn/{webauthn_id} | Get the WebAuthN enrollment specified by webauthn_id
[**list_totp_enrollment**](ChallengesApi.md#list_totp_enrollment) | **GET** /v1/challenge_enrollment/totp | List the totp enrollment results
[**list_webauthn_enrollments**](ChallengesApi.md#list_webauthn_enrollments) | **GET** /v1/challenge_enrollment/webauthn | List the webauthn enrollments
[**replace_challenge**](ChallengesApi.md#replace_challenge) | **PUT** /v1/challenges/{challenge_id} | Replace the challenge specified by challenge_id
[**update_totp_enrollment**](ChallengesApi.md#update_totp_enrollment) | **POST** /v1/challenge_enrollment/totp/{totp_id} | Update the totp_enrollment if the answer provided is correct.
[**update_webauthn_enrollment**](ChallengesApi.md#update_webauthn_enrollment) | **POST** /v1/challenge_enrollment/webauthn/{webauthn_id} | Update the WebAuthN enrollment if the answer provided is correct.


# **create_challenge**
> Challenge create_challenge(challenge)

create a challenge

Creates a challenge according to the provide specification. This challenge will persist for a period of time waiting for the challenge to be passed. It will eventually time out. 

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
    api_instance = agilicus_api.ChallengesApi(api_client)
    challenge = agilicus_api.Challenge() # Challenge | The challenge to create

    try:
        # create a challenge
        api_response = api_instance.create_challenge(challenge)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ChallengesApi->create_challenge: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **challenge** | [**Challenge**](Challenge.md)| The challenge to create | 

### Return type

[**Challenge**](Challenge.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully created the challenge. Depending on whether &#x60;send_now&#x60; was true, it could be waiting for an answer.  |  -  |
**400** | Error creating challenge. See error message body for more details. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_totp_enrollment**
> TOTPEnrollment create_totp_enrollment(totp_enrollment)

create a TOTP challenge enrollment

Creates a TOTP challenge enrollment. The returned body will contain the key the user needs to enroll in their application. The enrollment is not complete until the user provides a valid answer. 

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
    api_instance = agilicus_api.ChallengesApi(api_client)
    totp_enrollment = agilicus_api.TOTPEnrollment() # TOTPEnrollment | The TOTP challenge enrollment to create.

    try:
        # create a TOTP challenge enrollment
        api_response = api_instance.create_totp_enrollment(totp_enrollment)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ChallengesApi->create_totp_enrollment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **totp_enrollment** | [**TOTPEnrollment**](TOTPEnrollment.md)| The TOTP challenge enrollment to create. | 

### Return type

[**TOTPEnrollment**](TOTPEnrollment.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully created the TOTP challenge enrollment.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_webauthn_enrollment**
> WebAuthNEnrollment create_webauthn_enrollment(web_auth_n_enrollment)

create a WebAuthN challenge enrollment

Initiates a WebAuthN challenge enrollment. The enrollment is not complete until the user provides a valid answer. 

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
    api_instance = agilicus_api.ChallengesApi(api_client)
    web_auth_n_enrollment = agilicus_api.WebAuthNEnrollment() # WebAuthNEnrollment | The WebAuthN challenge enrollment to create.

    try:
        # create a WebAuthN challenge enrollment
        api_response = api_instance.create_webauthn_enrollment(web_auth_n_enrollment)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ChallengesApi->create_webauthn_enrollment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **web_auth_n_enrollment** | [**WebAuthNEnrollment**](WebAuthNEnrollment.md)| The WebAuthN challenge enrollment to create. | 

### Return type

[**WebAuthNEnrollment**](WebAuthNEnrollment.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully created the WebAuthN challenge enrollment.  |  -  |
**400** | Incorrect parameters supplied. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_challenge**
> delete_challenge(challenge_id)

Delete the challenge specified by challenge_id

Delete the challenge specified by challenge_id

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
    api_instance = agilicus_api.ChallengesApi(api_client)
    challenge_id = 'AbasaWlLLS' # str | A challenge id found in a path.

    try:
        # Delete the challenge specified by challenge_id
        api_instance.delete_challenge(challenge_id)
    except ApiException as e:
        print("Exception when calling ChallengesApi->delete_challenge: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **challenge_id** | **str**| A challenge id found in a path. | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Challenge was deleted |  -  |
**404** | Challenge not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_totp_enrollment**
> delete_totp_enrollment(totp_id, user_id=user_id)

Delete the TOTP enrollment specified by totp id

Delete the TOTP enrollment specified by totp id

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
    api_instance = agilicus_api.ChallengesApi(api_client)
    totp_id = 'AbasaWlLLS' # str | A totp id found in a path.
user_id = '1234' # str | Query based on user id (optional)

    try:
        # Delete the TOTP enrollment specified by totp id
        api_instance.delete_totp_enrollment(totp_id, user_id=user_id)
    except ApiException as e:
        print("Exception when calling ChallengesApi->delete_totp_enrollment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **totp_id** | **str**| A totp id found in a path. | 
 **user_id** | **str**| Query based on user id | [optional] 

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
**204** | Enrollment was deleted |  -  |
**404** | Enrollment not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_webauthn_enrollment**
> delete_webauthn_enrollment(webauthn_id, user_id=user_id)

Delete the WebAuthN enrollment specified by webauthn_id

Delete the WebAuthN enrollment specified by webauthn_id

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
    api_instance = agilicus_api.ChallengesApi(api_client)
    webauthn_id = 'AbasaWlLLS' # str | A webauthn id found in a path.
user_id = '1234' # str | Query based on user id (optional)

    try:
        # Delete the WebAuthN enrollment specified by webauthn_id
        api_instance.delete_webauthn_enrollment(webauthn_id, user_id=user_id)
    except ApiException as e:
        print("Exception when calling ChallengesApi->delete_webauthn_enrollment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **webauthn_id** | **str**| A webauthn id found in a path. | 
 **user_id** | **str**| Query based on user id | [optional] 

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
**204** | Enrollment was deleted |  -  |
**404** | Enrollment not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_answer**
> ChallengeAnswer get_answer(challenge_id, challenge_answer, challenge_uid, allowed, challenge_type)

answer a challenge

Checks whether the challenge answer is correct. If the challenge is not accepting answers, or the anwer is incorrect, a failure will be returned. Otherwise, the challenge will be considered answered and the user can log in. 

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
    api_instance = agilicus_api.ChallengesApi(api_client)
    challenge_id = 'AbasaWlLLS' # str | A challenge id found in a path.
challenge_answer = 'AbasaWlLLS' # str | The answer for the challenge
challenge_uid = 'AbasaWlLLS' # str | The user id for the challenge
allowed = false # bool | Whether the challenge was allowed. If true, then the user can proceed with the login. If false, then the user will be denied their login attempt. Set this to false if the login attempt was not desired. 
challenge_type = 'sms' # str | challenge method type query

    try:
        # answer a challenge
        api_response = api_instance.get_answer(challenge_id, challenge_answer, challenge_uid, allowed, challenge_type)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ChallengesApi->get_answer: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **challenge_id** | **str**| A challenge id found in a path. | 
 **challenge_answer** | **str**| The answer for the challenge | 
 **challenge_uid** | **str**| The user id for the challenge | 
 **allowed** | **bool**| Whether the challenge was allowed. If true, then the user can proceed with the login. If false, then the user will be denied their login attempt. Set this to false if the login attempt was not desired.  | 
 **challenge_type** | **str**| challenge method type query | 

### Return type

[**ChallengeAnswer**](ChallengeAnswer.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully answered the challenge. The user may now proceed with their login. |  -  |
**400** | The challenge answer failed. No particular reason will be given. |  -  |
**404** | Challenge not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_challenge**
> Challenge get_challenge(challenge_id)

Get the challenge specified by challenge_id

Get the challenge specified by challenge_id

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
    api_instance = agilicus_api.ChallengesApi(api_client)
    challenge_id = 'AbasaWlLLS' # str | A challenge id found in a path.

    try:
        # Get the challenge specified by challenge_id
        api_response = api_instance.get_challenge(challenge_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ChallengesApi->get_challenge: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **challenge_id** | **str**| A challenge id found in a path. | 

### Return type

[**Challenge**](Challenge.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return the challenge by id |  -  |
**404** | Challenge not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_totp_enrollment**
> TOTPEnrollment get_totp_enrollment(totp_id, user_id=user_id)

Get the TOTP enrollment specified by totp_id

Get the TOTP enrollment specified by totp_id

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
    api_instance = agilicus_api.ChallengesApi(api_client)
    totp_id = 'AbasaWlLLS' # str | A totp id found in a path.
user_id = '1234' # str | Query based on user id (optional)

    try:
        # Get the TOTP enrollment specified by totp_id
        api_response = api_instance.get_totp_enrollment(totp_id, user_id=user_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ChallengesApi->get_totp_enrollment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **totp_id** | **str**| A totp id found in a path. | 
 **user_id** | **str**| Query based on user id | [optional] 

### Return type

[**TOTPEnrollment**](TOTPEnrollment.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return the TOTP enrollment result by id |  -  |
**404** | Enrollment not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_webauthn_enrollment**
> WebAuthNEnrollment get_webauthn_enrollment(webauthn_id, user_id=user_id)

Get the WebAuthN enrollment specified by webauthn_id

Get the WebAuthN enrollment specified by webauthn_id

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
    api_instance = agilicus_api.ChallengesApi(api_client)
    webauthn_id = 'AbasaWlLLS' # str | A webauthn id found in a path.
user_id = '1234' # str | Query based on user id (optional)

    try:
        # Get the WebAuthN enrollment specified by webauthn_id
        api_response = api_instance.get_webauthn_enrollment(webauthn_id, user_id=user_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ChallengesApi->get_webauthn_enrollment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **webauthn_id** | **str**| A webauthn id found in a path. | 
 **user_id** | **str**| Query based on user id | [optional] 

### Return type

[**WebAuthNEnrollment**](WebAuthNEnrollment.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return the WebAuthN enrollment result by id |  -  |
**404** | Enrollment not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_totp_enrollment**
> ListTOTPEnrollmentResponse list_totp_enrollment(limit=limit, user_id=user_id)

List the totp enrollment results

List the totp enrollment results

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
    api_instance = agilicus_api.ChallengesApi(api_client)
    limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
user_id = '1234' # str | Query based on user id (optional)

    try:
        # List the totp enrollment results
        api_response = api_instance.list_totp_enrollment(limit=limit, user_id=user_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ChallengesApi->list_totp_enrollment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **user_id** | **str**| Query based on user id | [optional] 

### Return type

[**ListTOTPEnrollmentResponse**](ListTOTPEnrollmentResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return the TOTP enrollment results |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_webauthn_enrollments**
> ListWebAuthNEnrollmentResponse list_webauthn_enrollments(limit=limit, user_id=user_id)

List the webauthn enrollments

List the webauthn enrollments

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
    api_instance = agilicus_api.ChallengesApi(api_client)
    limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
user_id = '1234' # str | Query based on user id (optional)

    try:
        # List the webauthn enrollments
        api_response = api_instance.list_webauthn_enrollments(limit=limit, user_id=user_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ChallengesApi->list_webauthn_enrollments: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **user_id** | **str**| Query based on user id | [optional] 

### Return type

[**ListWebAuthNEnrollmentResponse**](ListWebAuthNEnrollmentResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return the WebAuthN enrollment results |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_challenge**
> Challenge replace_challenge(challenge_id, challenge)

Replace the challenge specified by challenge_id

Replace the challenge specified by challenge_id

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
    api_instance = agilicus_api.ChallengesApi(api_client)
    challenge_id = 'AbasaWlLLS' # str | A challenge id found in a path.
challenge = agilicus_api.Challenge() # Challenge | The challenge to replace. Note that some fields, such as user_id, cannot be modified.

    try:
        # Replace the challenge specified by challenge_id
        api_response = api_instance.replace_challenge(challenge_id, challenge)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ChallengesApi->replace_challenge: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **challenge_id** | **str**| A challenge id found in a path. | 
 **challenge** | [**Challenge**](Challenge.md)| The challenge to replace. Note that some fields, such as user_id, cannot be modified. | 

### Return type

[**Challenge**](Challenge.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The challenge was replaced. The result contains the updated challenge. |  -  |
**404** | Challenge not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_totp_enrollment**
> TOTPEnrollment update_totp_enrollment(totp_id, totp_enrollment_answer, user_id=user_id)

Update the totp_enrollment if the answer provided is correct.

Update the totp_enrollment if the answer provided is correct. This moves the state from pending to success.

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
    api_instance = agilicus_api.ChallengesApi(api_client)
    totp_id = 'AbasaWlLLS' # str | A totp id found in a path.
totp_enrollment_answer = agilicus_api.TOTPEnrollmentAnswer() # TOTPEnrollmentAnswer | The answer to the TOTP enrollment specified by totp_id.
user_id = '1234' # str | Query based on user id (optional)

    try:
        # Update the totp_enrollment if the answer provided is correct.
        api_response = api_instance.update_totp_enrollment(totp_id, totp_enrollment_answer, user_id=user_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ChallengesApi->update_totp_enrollment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **totp_id** | **str**| A totp id found in a path. | 
 **totp_enrollment_answer** | [**TOTPEnrollmentAnswer**](TOTPEnrollmentAnswer.md)| The answer to the TOTP enrollment specified by totp_id. | 
 **user_id** | **str**| Query based on user id | [optional] 

### Return type

[**TOTPEnrollment**](TOTPEnrollment.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The TOTP enrollment was was updated. |  -  |
**400** | Incorrect answer to enrollment challenge |  -  |
**404** | Enrollment not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_webauthn_enrollment**
> WebAuthNEnrollment update_webauthn_enrollment(webauthn_id, web_auth_n_enrollment_answer, user_id=user_id)

Update the WebAuthN enrollment if the answer provided is correct.

Update the WebAuthN enrollment if the answer provided is correct. This completes the device enrollment.

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
    api_instance = agilicus_api.ChallengesApi(api_client)
    webauthn_id = 'AbasaWlLLS' # str | A webauthn id found in a path.
web_auth_n_enrollment_answer = agilicus_api.WebAuthNEnrollmentAnswer() # WebAuthNEnrollmentAnswer | The answer to the WebAuthN enrollment specified by webauthn_id.
user_id = '1234' # str | Query based on user id (optional)

    try:
        # Update the WebAuthN enrollment if the answer provided is correct.
        api_response = api_instance.update_webauthn_enrollment(webauthn_id, web_auth_n_enrollment_answer, user_id=user_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ChallengesApi->update_webauthn_enrollment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **webauthn_id** | **str**| A webauthn id found in a path. | 
 **web_auth_n_enrollment_answer** | [**WebAuthNEnrollmentAnswer**](WebAuthNEnrollmentAnswer.md)| The answer to the WebAuthN enrollment specified by webauthn_id. | 
 **user_id** | **str**| Query based on user id | [optional] 

### Return type

[**WebAuthNEnrollment**](WebAuthNEnrollment.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The TOTP enrollment was was updated. |  -  |
**400** | Incorrect answer to enrollment challenge |  -  |
**404** | Enrollment not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

