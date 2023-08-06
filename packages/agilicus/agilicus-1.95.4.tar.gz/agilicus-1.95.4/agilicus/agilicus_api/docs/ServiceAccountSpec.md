# ServiceAccountSpec

The configuration object for a service account. A service account has the same properties of a user.
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the service account. This will be used as part of the generated email for the service account. Note the service account&#39;s email will not be updated after it has been created.  | 
**enabled** | **bool** | Enable/Disable a service account. This will enable/disable the service account user associated with this account. | [optional] 
**org_id** | **str** | The unique id of the Organisation to which this service account belongs to. This restricts the possible values for allowed_sub_orgs  | 
**allowed_sub_orgs** | **list[str]** | The list of suborgs that this service account can be used in. To enable this service account in a sub organisation, activate this service account&#39;s user in the organisation. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


