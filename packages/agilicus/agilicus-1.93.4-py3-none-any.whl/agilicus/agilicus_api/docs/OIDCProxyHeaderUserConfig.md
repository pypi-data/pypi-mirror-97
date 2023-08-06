# OIDCProxyHeaderUserConfig

The configuration for users to set header value, add header fields and remove existing header fields. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**set** | [**list[OIDCProxyHeaderMapping]**](OIDCProxyHeaderMapping.md) | The list of existing headers that will be set to new values. | [optional] 
**add** | [**list[OIDCProxyHeaderMapping]**](OIDCProxyHeaderMapping.md) | The list of headers (name and value) that will be added. | [optional] 
**remove** | [**list[OIDCProxyHeaderName]**](OIDCProxyHeaderName.md) | The list of header names that will be removed. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


