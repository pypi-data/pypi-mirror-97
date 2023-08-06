# UserIdentity

The core identity of a User in the system. Exactly one of these will exist per User.
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier | [optional] [readonly] 
**first_name** | **str** | User&#39;s first name | [optional] 
**last_name** | **str** | User&#39;s last name | [optional] 
**email** | **str** | User&#39;s email address | [optional] 
**type** | **str** | Type of user | [optional] [readonly] 
**upstream_user_identities** | [**list[UpstreamUserIdentity]**](UpstreamUserIdentity.md) | The upstream identities this user can use to log in to the system. When a user logs in, their identity in this system will be determined by matching against this list. Note that this implies that entries in this list are globally unique.  | [optional] [readonly] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


