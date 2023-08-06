# WebAuthNEnrollmentStatus

The status of the WebAuthN challenge enrollment.
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**challenge** | **str** | An opaque string used to challenge a user attempting to login using WebAuthN. The second factor device will return a signed version of this challenge to indicate that the user should be allowed to proceed.  | [optional] 
**credential_id** | **str** | A probabilistically-unique byte sequence identifying a public key credential source and its authentication assertions. See https://www.w3.org/TR/webauthn/#credential-id for more details  | [optional] 
**transports** | **list[str]** | List of supported transports for this enrolled credential | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


