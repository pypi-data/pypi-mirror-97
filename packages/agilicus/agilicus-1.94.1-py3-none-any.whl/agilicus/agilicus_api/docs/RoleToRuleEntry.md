# RoleToRuleEntry

Associates a rule with a role. The association may either be to include the rule in the role's effective list of rules, or it may be to exclude it. If the rule is excluded, then if an included role itself includes this rule, the rule will not be included in the final list of rules for this role. A rule can be included in a role only once. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**MetadataWithId**](MetadataWithId.md) |  | [optional] 
**spec** | [**RoleToRuleEntrySpec**](RoleToRuleEntrySpec.md) |  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


