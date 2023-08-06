# SessionsSpec

The information describing a session.
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_id** | **str** | The user id associated with the session | 
**org_id** | **str** | The org id associated with the issuer the user is logging into | 
**revoked** | **bool** | The status of a the session. A session is no longer valid if it has been revoked. | [optional] 
**number_of_logins** | **int** | The number of times a user has logged in during this session | [optional] 
**number_of_failed_multi_factor_challenges** | **int** | The number of times a user has failed a multi-factor authentication challenge associated with this session | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


