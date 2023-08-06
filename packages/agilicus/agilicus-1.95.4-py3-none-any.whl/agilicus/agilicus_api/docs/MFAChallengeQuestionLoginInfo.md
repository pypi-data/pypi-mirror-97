# MFAChallengeQuestionLoginInfo

The login information required when asking the Open Policy Agent to determine if a multi-factor authentication challenge should occur.
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_preference** | **str** | The user&#39;s preference regarding multi-factor authentication | [default to 'organisation_policy']
**client_id** | **str** | The common name of the client initiating the request on behalf of the user | 
**client_guid** | **str** | The guid of the client initiating the request on behalf of the user | 
**issuer_org_id** | **str** | The id of the organisation for the issuer the user is logging in through | 
**issuer_guid** | **str** | The guid of the issuer the user is logging into. | 
**org_id** | **str** | The id of the organisation the user is a member of | 
**user_id** | **str** | The id of the user requesting access | 
**user_object** | [**UserSummary**](UserSummary.md) |  | [optional] 
**login_session** | [**LoginSession**](LoginSession.md) |  | [optional] 
**upstream_idp** | **str** | The upstream IDP that the user is authenticating against | 
**ip_address** | **str** | The source ip address of the user&#39;s request. Both IPv4 and IPv6 address are supported | 
**amr_claim_present** | **bool** | Whether the amr claim is present in the response from the upstream | [default to False]
**last_mfa_login** | **datetime** | The time of the user&#39;s last successful multi-factor authenticated login | [optional] 
**user_mfa_preferences** | [**list[MFAChallengeMethod]**](MFAChallengeMethod.md) | The list of a user&#39;s multi-factor challenge methods | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


