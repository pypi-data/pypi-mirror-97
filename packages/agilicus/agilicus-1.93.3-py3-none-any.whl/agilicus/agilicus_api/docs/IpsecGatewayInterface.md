# IpsecGatewayInterface

An IPsec Gateway Interface 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name of the gateway interface. This name must be a legal RFC1123 label, and corresponds to the subdomain of the gateway interface.  | [optional] 
**hostname** | **str** | The hostname of the gateway interface. This is readOnly, and is generated from the name plus the gateway domain name.  | [optional] [readonly] 
**certificate_dn** | **str** | Certificate distinguished name (DN) subject of the gateway interface | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


