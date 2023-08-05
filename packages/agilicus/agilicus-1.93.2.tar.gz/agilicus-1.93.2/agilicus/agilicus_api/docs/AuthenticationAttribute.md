# AuthenticationAttribute

An attribute to be exposed for users authenticating against the system. Attributes allow the authentication subsystem to normalize a user's federated information to a format consumable by different systems. In particular, they map information related to the user to a single value in the record returning to the relying party in the authentication transaction. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attribute_name** | **str** | The of the attribute in the relying party&#39;s schema. Case sensitive. | 
**internal_attribute_path** | **str** | The object path to a field to use as the attribute. If the value is not present, null or empty, the attribute will be omitted.  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


