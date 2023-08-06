# FileSummary

Summary of file properties
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier | [optional] [readonly] 
**name** | **str** | Name of file | [optional] 
**tag** | **str** | A file tag | [optional] 
**label** | **str** | A file label | [optional] 
**size** | **int** | Size in bytes of the file | [optional] [readonly] 
**visibility** | [**FileVisibility**](FileVisibility.md) |  | [optional] 
**public_url** | **str** | The location of the file on the internet. If present, this file can be downloaded by requesting this URI. If the file is publically visible, then no credentials need be provided.  | [optional] [readonly] 
**storage_path** | **str** | Where the file is stored in the backend storage. | [optional] [readonly] 
**last_accessed** | **datetime** | Time object was last accessed | [optional] [readonly] 
**created** | **datetime** | Creation time | [optional] [readonly] 
**updated** | **datetime** | Update time | [optional] [readonly] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


