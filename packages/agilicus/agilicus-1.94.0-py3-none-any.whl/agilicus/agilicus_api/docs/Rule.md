# Rule

Rule's properties
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**host** | **str** | hostname to apply authz rule to. Deprecated. This is now inferred from the Environment or Service to which the rule belongs.  | [optional] 
**name** | **str** | A meaningful name to help identifiy the rule. This may be used to refer to it elsewhere, or to at a glace understand its purpose.  | 
**method** | **str** | The HTTP method to allow. | 
**path** | **str** | regex for HTTP path. Can be templatized with jinja2 using definitions collection. | 
**query_parameters** | [**list[RuleQueryParameter]**](RuleQueryParameter.md) | A set of constraints on the parameters specified in the query string. | [optional] 
**body** | [**RuleQueryBody**](RuleQueryBody.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


