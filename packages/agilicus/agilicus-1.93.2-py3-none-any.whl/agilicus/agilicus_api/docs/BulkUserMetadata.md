# BulkUserMetadata

The parameters for bulk setting metadata for a specific organisation and application. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**org_id** | **str** | The unique id of the Organisation to which this record applies.  | 
**app_id** | **str** | The unique id of the application to which this record applies.  | [optional] 
**name** | **str** | A descriptive name for this metadata entry | [optional] 
**data_type** | **str** | The type of data present in the configuration. This informs consumers of how to use the data present | 
**data** | **str** | The string representation of the data. This value is interpretted differently based on the data_type | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


