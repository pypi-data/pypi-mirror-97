# CertSigningReqStatus

The status for a CertSigningReq
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**certificates** | [**list[X509Certificate]**](X509Certificate.md) | The issued x509 certificates, formatted as PEM. This list is sorted by X509Certificate.not_before.  | [optional] 
**common_name** | **str** | The certificate common name (CN)  | [optional] [readonly] 
**dns_names** | **list[str]** | The list of domains of which the CSR is requesting to be issued to. | [optional] [readonly] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


