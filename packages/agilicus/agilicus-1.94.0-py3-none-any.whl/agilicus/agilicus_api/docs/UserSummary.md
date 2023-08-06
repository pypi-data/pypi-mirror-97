# UserSummary

A per-organisation view of a user. This will contain properties associated with a user that are specific to the organisation with which they are interacting. Note that many of the properties are inherited from the UserIdentity of the user. These may not be modified. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier | [optional] [readonly] 
**external_id** | **str** | External unique identifier | [optional] 
**enabled** | **bool** | Enable/Disable a user | [optional] 
**status** | [**UserStatusEnum**](UserStatusEnum.md) |  | [optional] 
**first_name** | **str** | User&#39;s first name | [optional] 
**last_name** | **str** | User&#39;s last name | [optional] 
**email** | **str** | User&#39;s email address | [optional] 
**provider** | **str** | Upstream IdP name | [optional] 
**roles** | [**Roles**](Roles.md) |  | [optional] 
**org_id** | **str** | Unique identifier | [optional] 
**type** | **str** | Type of user | [optional] [readonly] 
**created** | **datetime** | Creation time | [optional] [readonly] 
**updated** | **datetime** | Update time | [optional] [readonly] 
**auto_created** | **bool** | Whether the user was automatically created as part of another process such as logging in. On creation, this flag being true serves to trigger any behaviour tied to automatically created users, such as addition to special groups. On read, it can serve to indicate whether the user was automatically created. On update it will ensure that the automatically triggered behaviour still holds true.  | [optional] [default to False]
**upstream_user_identities** | [**list[UpstreamUserIdentity]**](UpstreamUserIdentity.md) | The upstream identities this user can use to log in to the system. When a user logs in, their identity in this system will be determined by matching against this list. Note that this implies that entries in this list are globally unique.  | [optional] [readonly] 
**cascade** | **bool** | Whether the user will be added to sub organisations automatically. When set for a user that is a member of a particular organisation, subsequent creations of sub organisations will add this user to that suborgansation.  | [optional] [default to False]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


