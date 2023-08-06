# APIKeyStatus

Runtime information about the APIKey. The jti is the ID of the token corresponding to this API Key. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**api_key** | **str** | The value to use as the password in the basic authentication flow. Note that this value will only be present in the APIKeyStatus when creating the API Key. It is omitted in future requests to prevent it from leaking. Treat this key like any other password: keep it secret; keep it safe.  | [optional] 
**token_id** | **str** | Unique identifier | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


