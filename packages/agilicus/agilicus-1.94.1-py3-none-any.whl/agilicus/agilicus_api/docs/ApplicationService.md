# ApplicationService

Application service's properties
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created** | **datetime** | Creation time | [optional] [readonly] 
**id** | **str** | Unique identifier | [optional] [readonly] 
**name** | **str** | The name of the service. Services will be selected and assigned using this. This value must be unique within an organisation.  | 
**org_id** | **str** | The organisation which owns this service. | 
**hostname** | **str** | The hostname of the service. Your applications will refer to this service using its hostname. This can also be the IP Address of the service. If the address is an IPv4 Address it will add the IP to the ipv4_addresses field and set the name_resolution to static  | [optional] 
**ipv4_addresses** | **list[str]** | The IPv4 addresses of &#x60;hostname&#x60; within the data center. | [optional] 
**name_resolution** | **str** | How to resolve the hostname of the service. If static, then ipv4_address will be used. Otherwise, if dns the Organisation&#39;s dns services will be queried.  | [optional] [default to 'static']
**port** | **int** | The transport-layer port on which to access the service. exclusiveMinimum: 0 exclusiveMaximum: 65536  | [optional] 
**protocol** | **str** | The transport-layer protocol over which to communicate with the service.  | [optional] [default to 'tcp']
**assignments** | [**list[ApplicationServiceAssignment]**](ApplicationServiceAssignment.md) | The Application Environments which have access to this ApplicationService. Manipulate this list to add or remove access to the ApplicationService.  | [optional] 
**updated** | **datetime** | Update time | [optional] [readonly] 
**service_type** | **str** | The type of application service. This refers to how the application connects to the service | [optional] 
**service_protocol_type** | **str** | The protocol carried by this service. This indicates to the Agilicus infrastructure how to interpret the data being transmitted to the service. Different protocols have different subclasses of an ApplicationService used to configure that protocol&#39;s details. This field may take on the following values:   - ip: Any upper layer protocols are transparent to the Agilicus infrastructure.     Agilicus does not participate in the protocol.   - fileshare: The service is a fileshare. Agilicus will participate in the file sharing     protocol in order to expose the fileshare to the Internet.  | [optional] [readonly] 
**connector_id** | **str** | Unique identifier | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


