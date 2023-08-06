# Service

A Service defines a multitenant application which is operated by Agilicus. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created** | **datetime** | Creation time | [optional] [readonly] 
**id** | **str** | Unique identifier | [optional] [readonly] 
**name** | **str** | Service name. Must be unique accross all Applications and Services. | 
**description** | **str** | Service description text | [optional] 
**org_id** | **str** | organisation id | 
**contact_email** | **str** | Administrator contact email | [optional] 
**roles** | [**RoleList**](RoleList.md) |  | [optional] 
**definitions** | [**list[Definition]**](Definition.md) | List of definitions | [optional] 
**base_url** | **str** | The URL which forms the base of this service. This value will be joined with the paths in the rules for this service to form its authorization model.  | 
**updated** | **datetime** | Update time | [optional] [readonly] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


