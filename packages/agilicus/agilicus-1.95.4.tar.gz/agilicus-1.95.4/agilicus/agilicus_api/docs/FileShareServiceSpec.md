# FileShareServiceSpec

The configurable properties of a FileShareService. Since multiple file shares will be exposed using the same host, no two FileShareServices in the same organisation may have the same share_name. The connector_id controls which connector will be used to expose this file share. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the service. This uniquely identifies the service within the organisation.  | 
**share_name** | **str** | The name of the share as exposed to the Internet. This will be used to build the URI used to mount the share. The share_name is unique among the file shares of the organisation.  | 
**org_id** | **str** | Unique identifier | 
**local_path** | **str** | The path to the directory to share on the local file system. This should point to a directory, not a file. Use a slash (&#39;/&#39;, U+002F) to separate directories within the path.  | 
**connector_id** | **str** | Unique identifier | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


