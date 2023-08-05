# HttpRule

A rule condition applied to the attributes of an http request.
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**rule_type** | **str** | Used to distinguish between different types of rule | [default to 'HttpRule']
**methods** | **list[str]** | The HTTP methods to allow. If any of the listed methods are matched, then this portion of the rule matches.  | [optional] 
**path_regex** | **str** | regex for HTTP path. Can be templatized with jinja2 using definitions collection. | [optional] 
**query_parameters** | [**list[RuleQueryParameter]**](RuleQueryParameter.md) | A set of constraints on the parameters specified in the query string. | [optional] 
**body** | [**RuleQueryBody**](RuleQueryBody.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


