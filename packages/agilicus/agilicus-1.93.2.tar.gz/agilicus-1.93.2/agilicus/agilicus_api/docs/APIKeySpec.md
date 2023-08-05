# APIKeySpec

The definition of an API Key. This controls how it behaves. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_id** | **str** | Unique identifier | 
**org_id** | **str** | Unique identifier | 
**expiry** | **datetime** | The API Key expiry time in UTC. If ommitted the key does not expire. | [optional] 
**session** | **str** | Unique identifier | [optional] 
**scopes** | **list[str]** | The list of scopes requested for APIKey. Ex. urn:agilicus:users. An optional scope is specified with an ? at the end. Optional scopes are used when the permission is requested but not required. Ex. urn:agilicus:users?. A non-optional scope will cause creation of this API Key to fail if the user does not have that permission in this org.  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


