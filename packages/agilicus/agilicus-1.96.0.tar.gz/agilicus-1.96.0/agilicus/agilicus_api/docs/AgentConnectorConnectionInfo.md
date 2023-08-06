# AgentConnectorConnectionInfo

Connection information pertaining to a Connector
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**connection_uri** | **str** | The URI used to establish a connection to the connector. | [optional] 
**connection_location** | **str** | The location (e.g. fully qualified domain name) of the connection. While this matches the location in the &#x60;connection_uri&#x60;, it is provided separately for convenience.  | [optional] 
**connection_path** | **str** | The path of the connection. While this matches the path in the &#x60;connection_uri&#x60;, it is provided separately for convenience.  | [optional] 
**connection_org_id** | **str** | The identifier for the organisation hosting the server side of this connection.  | [optional] 
**connection_app_name** | **str** | The name of the Application (if any) hosting the server side of this connection. Note that not all servers will be hosted by an Application, in which case this will be empty.  | [optional] 
**end_to_end_tls** | **bool** | Controls if the connection is end to end TLS.  | [optional] 
**max_number_connections** | **int** | The maximum number of connections to maintain to the cluster when stable. Note that this value may be exceeded during times of reconfiguration. A value of zero means that the connection is effectively unused by this Secure Agent.  | [optional] [default to 16]
**ip_services** | [**list[ApplicationService]**](ApplicationService.md) | The list of ip services associated with this connection | [optional] 
**file_share_services** | [**list[FileShareService]**](FileShareService.md) | The list of fileshare services associated with this connection | [optional] 
**application_config** | [**ApplicationConfig**](ApplicationConfig.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


