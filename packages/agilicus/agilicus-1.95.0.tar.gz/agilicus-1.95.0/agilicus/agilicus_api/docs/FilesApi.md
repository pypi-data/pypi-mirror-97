# agilicus_api.FilesApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_file**](FilesApi.md#add_file) | **POST** /v1/files | upload a file
[**delete_file**](FilesApi.md#delete_file) | **DELETE** /v1/files/{file_id} | Delete a File
[**get_download**](FilesApi.md#get_download) | **GET** /v1/files_download/{file_id} | Download File
[**get_file**](FilesApi.md#get_file) | **GET** /v1/files/{file_id} | Get File metadata
[**list_files**](FilesApi.md#list_files) | **GET** /v1/files | Query Files
[**replace_file**](FilesApi.md#replace_file) | **PUT** /v1/files/{file_id} | Update a file


# **add_file**
> FileSummary add_file(name, file_zip, org_id=org_id, tag=tag, label=label, region=region, visibility=visibility, md5_hash=md5_hash)

upload a file

Upload a file

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.FilesApi(api_client)
    name = 'name_example' # str | Name of file
file_zip = '/path/to/file' # file | The contents of the file in binary format
org_id = 'org_id_example' # str | Unique identifier (optional)
tag = 'tag_example' # str | A file tag (optional)
label = 'label_example' # str | A file label (optional)
region = agilicus_api.StorageRegion() # StorageRegion |  (optional)
visibility = agilicus_api.FileVisibility() # FileVisibility |  (optional)
md5_hash = 'md5_hash_example' # str | MD5 Hash of file in base64 (optional)

    try:
        # upload a file
        api_response = api_instance.add_file(name, file_zip, org_id=org_id, tag=tag, label=label, region=region, visibility=visibility, md5_hash=md5_hash)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->add_file: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| Name of file | 
 **file_zip** | **file**| The contents of the file in binary format | 
 **org_id** | **str**| Unique identifier | [optional] 
 **tag** | **str**| A file tag | [optional] 
 **label** | **str**| A file label | [optional] 
 **region** | [**StorageRegion**](StorageRegion.md)|  | [optional] 
 **visibility** | [**FileVisibility**](FileVisibility.md)|  | [optional] 
 **md5_hash** | **str**| MD5 Hash of file in base64 | [optional] 

### Return type

[**FileSummary**](FileSummary.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully uploaded file |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_file**
> delete_file(file_id, org_id=org_id)

Delete a File

Delete a File

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.FilesApi(api_client)
    file_id = '1234' # str | file_id path
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Delete a File
        api_instance.delete_file(file_id, org_id=org_id)
    except ApiException as e:
        print("Exception when calling FilesApi->delete_file: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_id** | **str**| file_id path | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | File was deleted |  -  |
**404** | File does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_download**
> file get_download(file_id, org_id=org_id)

Download File

Download File

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.FilesApi(api_client)
    file_id = '1234' # str | file_id path
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Download File
        api_response = api_instance.get_download(file_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->get_download: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_id** | **str**| file_id path | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

**file**

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/octet-stream

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Downloaded |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_file**
> FileSummary get_file(file_id, org_id=org_id)

Get File metadata

Get File metadata

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.FilesApi(api_client)
    file_id = '1234' # str | file_id path
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Get File metadata
        api_response = api_instance.get_file(file_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->get_file: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_id** | **str**| file_id path | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**FileSummary**](FileSummary.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return File by id |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_files**
> ListFilesResponse list_files(limit=limit, org_id=org_id, user_id=user_id, tag=tag)

Query Files

Query Files

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.FilesApi(api_client)
    limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
org_id = '1234' # str | Organisation Unique identifier (optional)
user_id = '1234' # str | Query based on user id (optional)
tag = 'theme' # str | Search files based on tag (optional)

    try:
        # Query Files
        api_response = api_instance.list_files(limit=limit, org_id=org_id, user_id=user_id, tag=tag)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->list_files: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **user_id** | **str**| Query based on user id | [optional] 
 **tag** | **str**| Search files based on tag | [optional] 

### Return type

[**ListFilesResponse**](ListFilesResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return files list |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_file**
> FileSummary replace_file(file_id, file, org_id=org_id)

Update a file

Update a file

### Example

* Bearer (JWT) Authentication (token-valid):
```python
from __future__ import print_function
import time
import agilicus_api
from agilicus_api.rest import ApiException
from pprint import pprint
configuration = agilicus_api.Configuration()
# Configure Bearer authorization (JWT): token-valid
configuration.access_token = 'YOUR_BEARER_TOKEN'

# Defining host is optional and default to https://api.agilicus.com
configuration.host = "https://api.agilicus.com"
# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = agilicus_api.FilesApi(api_client)
    file_id = '1234' # str | file_id path
file = '/path/to/file' # File | Upload file request
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Update a file
        api_response = api_instance.replace_file(file_id, file, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->replace_file: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_id** | **str**| file_id path | 
 **file** | [**File**](File.md)| Upload file request | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**FileSummary**](FileSummary.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | File was updated |  -  |
**404** | File does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

