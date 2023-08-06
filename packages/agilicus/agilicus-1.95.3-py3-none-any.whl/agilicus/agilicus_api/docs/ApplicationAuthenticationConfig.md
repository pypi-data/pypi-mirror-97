# ApplicationAuthenticationConfig

The configuration for application authentication options. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**application_handles_authentication** | **bool** | Whether the application should be forwarded requests when a user is unauthenticated so that the application can trigger authentication. If true, unauthenticated user requests will be forwarded to the application with a header indicating the user is unauthenticated. If false unauthenticated users will be denied and no traffic will reach the application.  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


