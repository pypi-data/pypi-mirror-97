# PolicyRuleSpec

A rule to be evaluated by the policy engine.
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | A descriptive name of the policy rule to help administrators identify each rule. A name should describe the business logic the rule is satisfying. | [optional] 
**action** | **str** | The action to take if the conditions are evaluated to true. Actions are case sensitive. | 
**priority** | **int** | This field is deprecated. The priority of this rule relative to other rules. Rules of a higher priority will be evaluated first and if the condition evaluates to true the action will be taken. 1 is the highest priority. | [optional] [default to 1]
**org_id** | **str** | The org id corresponding to the issuer whose policy you are updating | [optional] 
**conditions** | [**list[PolicyCondition]**](PolicyCondition.md) | An array mapping a condition type to a condition. | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


