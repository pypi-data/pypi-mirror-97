# ListUserRolesForAnOrg

Response object for org user roles query. This is all roles a user has for a given org. Note this does not include roles inherited via group membership. A user may have multiple roles for a given application. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**org_user_roles** | [**list[UserRolesForAnOrg]**](UserRolesForAnOrg.md) | The matching UserRolesForAnOrgs objects | 
**limit** | **int** | Limit on the number of rows in the response | 
**offset** | **int** | The offset of the next data entry. A value of offset equal to the limit implies there might be more data available and the client should query again with the offset query parameter set to this value.  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


