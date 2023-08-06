# PolicyGroupSpec

A policy group consists of a list of rules.
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the group | [optional] 
**rule_ids** | **list[str]** | A list of PolicyRule ids that make up the policy group. The rules are evaluated based on the priority of their action. The ordering is as follows allow_login, deny_login, dont_mfa, authenticate, do_mfa The first rule that matches will take that rules action.  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


