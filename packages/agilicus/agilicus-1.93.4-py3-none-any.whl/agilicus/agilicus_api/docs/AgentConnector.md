# AgentConnector

A secure agent connector establishes a tunnel between the Agilicus infrastructure and the Secure Agent running on site. Its configuration controls how that link is established, how many connections are maintained and so on. Typically a connector corresponds to an Application running in the Agilicus infrastructure which provides the ingress side of the Secure Agent tunnel. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**MetadataWithId**](MetadataWithId.md) |  | [optional] 
**spec** | [**AgentConnectorSpec**](AgentConnectorSpec.md) |  | 
**status** | [**AgentConnectorStatus**](AgentConnectorStatus.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


