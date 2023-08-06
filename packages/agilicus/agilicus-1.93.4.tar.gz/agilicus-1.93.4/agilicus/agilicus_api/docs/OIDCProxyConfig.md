# OIDCProxyConfig

The configuration for OIDC-Proxy to set/substitute headers, set domain name mappings, set authentification configurations if auth is enabled and manipulate content based on its type. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**headers** | [**OIDCProxyHeader**](OIDCProxyHeader.md) |  | 
**domain_mapping** | [**OIDCProxyDomainMapping**](OIDCProxyDomainMapping.md) |  | 
**auth** | [**OIDCAuthConfig**](OIDCAuthConfig.md) |  | [optional] 
**content_manipulation** | [**OIDCProxyContentManipulation**](OIDCProxyContentManipulation.md) |  | 
**upstream_config** | [**OIDCProxyUpstreamConfig**](OIDCProxyUpstreamConfig.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


