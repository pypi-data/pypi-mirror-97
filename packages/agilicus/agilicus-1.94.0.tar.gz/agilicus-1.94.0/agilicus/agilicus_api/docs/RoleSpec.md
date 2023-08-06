# RoleSpec

The specification of a `RoleV2`.
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**app_id** | **str** | Unique identifier | [optional] 
**name** | **str** | A descriptive name of the role. This will be used to reference the role, in the context of the application, from other systems. Roles are case sensitive.  | 
**comments** | **str** | A description of the role. The comments have no functional effect, but can help to clarify the purpose of a role when the name is not sufficient.  | [optional] 
**included** | [**list[IncludedRole]**](IncludedRole.md) | A list of included rules for the role. This role will grant permissions for all rules associated directly with itself, and with its included roles. Note that the inclusion is recursive: a role will get the rules of roles it includes, and the roles that they include, and so on. The roles are included by ID  | [optional] 
**org_id** | **str** | Unique identifier | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


