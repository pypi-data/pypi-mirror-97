# IpsecConnectionSpec

An IPsec specification for a connection. A connection is made from Agilicus cloud (local) to the customer (remote). 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ike_version** | **str** | The IKE version | [optional] 
**remote_ipv4_address** | **str** | remote peer IPv4 address | [optional] 
**remote_dns_ipv4_address** | **str** | remote peer DNS IPv4 address | [optional] 
**remote_healthcheck_ipv4_address** | **str** | Remote peer healthcheck IPv4 address. The remote peer address must respond to ping (ICMP). This is used to validate the health of the connection.  | [optional] 
**ike_cipher_encryption_algorithm** | [**CipherEncryptionAlgorithm**](CipherEncryptionAlgorithm.md) |  | [optional] 
**ike_cipher_integrity_algorithm** | [**CipherIntegrityAlgorithm**](CipherIntegrityAlgorithm.md) |  | [optional] 
**ike_cipher_diffie_hellman_group** | [**CipherDiffieHellmanGroup**](CipherDiffieHellmanGroup.md) |  | [optional] 
**esp_cipher_encryption_algorithm** | [**CipherEncryptionAlgorithm**](CipherEncryptionAlgorithm.md) |  | [optional] 
**esp_cipher_integrity_algorithm** | [**CipherIntegrityAlgorithm**](CipherIntegrityAlgorithm.md) |  | [optional] 
**esp_cipher_diffie_hellman_group** | [**CipherDiffieHellmanGroup**](CipherDiffieHellmanGroup.md) |  | [optional] 
**esp_lifetime** | **int** | Absolute time after which an IPsec security association expires, in minutes.  | [optional] 
**ike_lifetime** | **int** | Absolute time after which an IKE security association expires, in minutes.  | [optional] 
**ike_rekey** | **bool** | Allows control of IKE rekey.  true is enabled, false is disabled.  | [optional] 
**ike_reauth** | **bool** | Allows control of IKE re-authentication.  true is enabled, false is disabled.  | [optional] 
**ike_authentication_type** | **str** | The IKE authentication type. | [optional] 
**ike_preshared_key** | **str** | ike preshared key | [optional] 
**ike_chain_of_trust_certificates** | **str** | Chain of trust certficates. Certificates are PEM encoded and are separated by a newline.  ie. A signed by B would be a string where A is first, newline, followed by B.  | [optional] 
**ike_certificate_dn** | **str** | certificate distinguished name (DN) | [optional] 
**local_ipv4_block** | **str** | The local IP block that used by the tunnel. A tunnel requires a /30 subnet, within the following IP address ranges    192.168.0.0 -&gt; 192.168.255.252   172.16.0.0 -&gt; 172.31.255.255  | [optional] 
**remote_ipv4_ranges** | [**list[IpsecConnectionIpv4Block]**](IpsecConnectionIpv4Block.md) | One or more IP address ranges that define the peer network range.  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


