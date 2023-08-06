# OIDCUpstreamIdentityProvider

Custom OIDC Upstream Identity Provider
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | A name used to uniquely refer to the upstream identity provider configuration. This is the text that will be displayed when presenting the upstream identity for login. | 
**icon** | **str** | The icon file to be used, limited to: numbers, letters, underscores, hyphens and periods. It is part of a css class (with the periods replaced by underscores).  To use a custom icon than the provided default you will need to add the icon the static/img folder and update the static css file to add a new css button like below &#x60;&#x60;&#x60;json .dex-btn-icon--&lt;your-logo_svg&gt; {   background-image: url(../static/img/&lt;your-logo.svg&gt;); } &#x60;&#x60;&#x60;  To use a default icon simply enter an icon name from the pre-provided defaults found in the static/img folder The default icons are   - bitbucket   - coreos   - email   - github   - gitlab   - google   - ldap   - linkedin   - microsoft   - oidc   - saml  | [optional] 
**issuer** | **str** | The upstream issuer uri. This is the URI which identifies the issuer against which users selecting this OIDCUpstreamIdentityProvider will authenticate. The issuer must support the OpenID Connect discovery document described here: https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderConfig. | 
**client_id** | **str** | The client ID for the upstream identity provider | 
**client_secret** | **str** | The secret presented to the upstream during any workflows which require authentication | [optional] 
**issuer_external_host** | **str** | A proxy standing in for the main issuer host. Use this if fronting the upstream through the Agilicus infrastructure | [optional] 
**username_key** | **str** | Allows changing the key in the OIDC response claims used to determine the full name of the user. If not present, defaults to the standard name | [optional] 
**email_key** | **str** | Allows changing the key in the OIDC response claims used to determine the email address of the user. If not present, defaults to the standard email | [optional] 
**email_verification_required** | **bool** | Controls whether email verification is required for this OIDC provider. Some OIDC providers do not take steps to verify the email address of users, or may not do so in all cases. Setting this value to true will reject any successful upstream logins for users which have not had their email address verified. | [optional] [default to True]
**request_user_info** | **bool** | Controls whether the system will retrieve extra information about the user from the provider&#39;s user_info endpoint. This can be useful if the initial OIDC response does not contain sufficient information to determine the email address or user&#39;s name. Setting this value to true will cause extra requests to be generated to the upstream every time a user logs in to it. | [optional] 
**user_id_key** | **str** | Changes the key used to determine the id of the user in this upstream. The key will be used to retrieve the user id from the id token claims returned from the upstream when the user logs in. This user id is in turn used to link the user to its identity within the system. If not present, the system will fall back on the default, which is &#x60;sub&#x60;.  | [optional] 
**auto_create_status** | [**AutoCreateStatus**](AutoCreateStatus.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


