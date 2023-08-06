# agilicus_api.PolicyApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_challenge_decision**](PolicyApi.md#get_challenge_decision) | **POST** /v1/data/authentication/mfa_policy/allow | evaluate a policy challenge decision
[**get_enrollment_decision**](PolicyApi.md#get_enrollment_decision) | **POST** /v1/data/authentication/enrollment/allow | evaluate a policy enrollment decision
[**map_attributes**](PolicyApi.md#map_attributes) | **POST** /v1/data/authentication/attribute_mapping/map_attributes | map attributes of a user


# **get_challenge_decision**
> MFAChallengeAnswer get_challenge_decision(mfa_challenge_question)

evaluate a policy challenge decision

Evaluate a policy challenge decision to determine if the user should be forced to answer a challenge

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
    api_instance = agilicus_api.PolicyApi(api_client)
    mfa_challenge_question = agilicus_api.MFAChallengeQuestion() # MFAChallengeQuestion | The MFA Challenge Question to ask

    try:
        # evaluate a policy challenge decision
        api_response = api_instance.get_challenge_decision(mfa_challenge_question)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling PolicyApi->get_challenge_decision: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **mfa_challenge_question** | [**MFAChallengeQuestion**](MFAChallengeQuestion.md)| The MFA Challenge Question to ask | 

### Return type

[**MFAChallengeAnswer**](MFAChallengeAnswer.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The challenge policy evaluation was successful |  -  |
**400** | Bad request. See https://www.openpolicyagent.org/docs/latest/rest-api/#get-a-document for details |  -  |
**500** | Server Error. See https://www.openpolicyagent.org/docs/latest/rest-api/#get-a-document for details |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_enrollment_decision**
> MFAEnrollmentAnswer get_enrollment_decision(mfa_enrollment_question)

evaluate a policy enrollment decision

Evaluate a policy enrollment decision to determine if the user should be forced to enroll

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
    api_instance = agilicus_api.PolicyApi(api_client)
    mfa_enrollment_question = agilicus_api.MFAEnrollmentQuestion() # MFAEnrollmentQuestion | The MFA Enrollment Question to ask

    try:
        # evaluate a policy enrollment decision
        api_response = api_instance.get_enrollment_decision(mfa_enrollment_question)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling PolicyApi->get_enrollment_decision: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **mfa_enrollment_question** | [**MFAEnrollmentQuestion**](MFAEnrollmentQuestion.md)| The MFA Enrollment Question to ask | 

### Return type

[**MFAEnrollmentAnswer**](MFAEnrollmentAnswer.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The enrollment policy evaluation was successful |  -  |
**400** | Bad request. See https://www.openpolicyagent.org/docs/latest/rest-api/#get-a-document for details |  -  |
**500** | Server Error. See https://www.openpolicyagent.org/docs/latest/rest-api/#get-a-document for details |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **map_attributes**
> MapAttributesAnswer map_attributes(map_attributes_question)

map attributes of a user

map attributes of a user

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
    api_instance = agilicus_api.PolicyApi(api_client)
    map_attributes_question = agilicus_api.MapAttributesQuestion() # MapAttributesQuestion | The attributes to map and information used to gather them

    try:
        # map attributes of a user
        api_response = api_instance.map_attributes(map_attributes_question)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling PolicyApi->map_attributes: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **map_attributes_question** | [**MapAttributesQuestion**](MapAttributesQuestion.md)| The attributes to map and information used to gather them | 

### Return type

[**MapAttributesAnswer**](MapAttributesAnswer.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The attributes were mapped successfully |  -  |
**400** | Bad request. See https://www.openpolicyagent.org/docs/latest/rest-api/#get-a-document for details |  -  |
**500** | Server Error. See https://www.openpolicyagent.org/docs/latest/rest-api/#get-a-document for details |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

