# ListUsersResponse

Response object for user query
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**users** | [**list[User]**](User.md) | List of User objects | [optional] 
**limit** | **int** | Limit on the number of rows in the response | 
**previous_page_email** | **str** | The first email on the current page. Can be used with \&quot;backwards\&quot; as the search_direction_query parameter to retrieve the previous page&#39;s entries. Is an empty string if the current page is the first page.  | [optional] 
**next_page_email** | **str** | The first email on the next page. Can be used with \&quot;forwards\&quot; as the search_direction_query parameter to retrieve the next page&#39;s entries. Is an empty string if the current page is the last page.  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


