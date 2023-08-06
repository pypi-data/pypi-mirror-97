# FileShareService

A web-based file share exposed via the Agilicus Cloud. The share will be exposed via a files host with path `/{spec.share_name}`. A file share will create an associated ApplicationService which links it to the chosen Connector.  Multiple connectors may be used to expose file shares. This can be useful if two file shares are on different systems when using a connector with a local component such as an AgentConnector. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**MetadataWithId**](MetadataWithId.md) |  | [optional] 
**spec** | [**FileShareServiceSpec**](FileShareServiceSpec.md) |  | 
**status** | [**FileShareServiceStatus**](FileShareServiceStatus.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


