# OrganisationStateStatus

The status of an organisation. The state of an organisation controls the availability of resources in an organisation. Depending on the state of the organisation administrative tools, the agilicus federated authentication plaform, as well as any applications provided could be disabled.   * `active`: This organisation is operational and all components are running.   * `suspended`: The applications run by the this organisation are not running, however     the administrative and self serve tools are still accessable. This org can still be managed     and resumed at some point.   * `disabled`: Neither applications nor administrative tools are running for this organisation. This org can only be managed     by agilicus.   * `deleted`: This organisation has been deleted and objects in the Agilicus API may not exist at all. No applications     or administrative tools are running for this organisation. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


