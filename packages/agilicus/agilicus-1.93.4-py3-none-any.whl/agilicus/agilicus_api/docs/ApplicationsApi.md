# agilicus_api.ApplicationsApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_config**](ApplicationsApi.md#add_config) | **POST** /v2/applications/{app_id}/environments/{env_name}/configs | Add an environment configuration row
[**add_role**](ApplicationsApi.md#add_role) | **POST** /v2/applications/{app_id}/roles | Add a role to the application.
[**add_role_to_rule_entry**](ApplicationsApi.md#add_role_to_rule_entry) | **POST** /v2/applications/{app_id}/role_to_rule_entries | Add a rule to a role in the application.
[**add_rule**](ApplicationsApi.md#add_rule) | **POST** /v2/applications/{app_id}/rules | Add a rule to the application.
[**create_agent**](ApplicationsApi.md#create_agent) | **POST** /v2/secure_agents | Create a secure agent
[**create_application**](ApplicationsApi.md#create_application) | **POST** /v2/applications | Create an application
[**delete_agent**](ApplicationsApi.md#delete_agent) | **DELETE** /v2/secure_agents/{agent_id} | Delete a secure agent
[**delete_application**](ApplicationsApi.md#delete_application) | **DELETE** /v2/applications/{app_id} | Remove an application
[**delete_config**](ApplicationsApi.md#delete_config) | **DELETE** /v2/applications/{app_id}/environments/{env_name}/configs/{env_config_id} | Remove an environment configuration
[**delete_role**](ApplicationsApi.md#delete_role) | **DELETE** /v2/applications/{app_id}/roles/{role_id} | Remove a role
[**delete_role_to_rule_entry**](ApplicationsApi.md#delete_role_to_rule_entry) | **DELETE** /v2/applications/{app_id}/role_to_rule_entries/{role_to_rule_entry_id} | Remove a role_to_rule_entry
[**delete_rule**](ApplicationsApi.md#delete_rule) | **DELETE** /v2/applications/{app_id}/rules/{rule_id} | Remove a rule
[**get_agent**](ApplicationsApi.md#get_agent) | **GET** /v2/secure_agents/{agent_id} | Get a secure agent
[**get_application**](ApplicationsApi.md#get_application) | **GET** /v2/applications/{app_id} | Get a application
[**get_config**](ApplicationsApi.md#get_config) | **GET** /v2/applications/{app_id}/environments/{env_name}/configs/{env_config_id} | Get environment configuration
[**get_environment**](ApplicationsApi.md#get_environment) | **GET** /v2/applications/{app_id}/environments/{env_name} | Get an environment
[**get_role**](ApplicationsApi.md#get_role) | **GET** /v2/applications/{app_id}/roles/{role_id} | Get a role
[**get_role_to_rule_entry**](ApplicationsApi.md#get_role_to_rule_entry) | **GET** /v2/applications/{app_id}/role_to_rule_entries/{role_to_rule_entry_id} | Get a role_to_rule_entry
[**get_rule**](ApplicationsApi.md#get_rule) | **GET** /v2/applications/{app_id}/rules/{rule_id} | Get a rule
[**list_agents**](ApplicationsApi.md#list_agents) | **GET** /v2/secure_agents | List secure agents
[**list_application_summaries**](ApplicationsApi.md#list_application_summaries) | **GET** /v2/application_summaries | List application summaries
[**list_applications**](ApplicationsApi.md#list_applications) | **GET** /v2/applications | Get applications
[**list_combined_rules**](ApplicationsApi.md#list_combined_rules) | **GET** /v2/combined_rules | List rules combined by scope or role
[**list_configs**](ApplicationsApi.md#list_configs) | **GET** /v2/applications/{app_id}/environments/{env_name}/configs | Get all environment configuration
[**list_environment_configs_all_apps**](ApplicationsApi.md#list_environment_configs_all_apps) | **GET** /v2/environment_configs | Get all environment configuration for a given organisation.
[**list_role_to_rule_entries**](ApplicationsApi.md#list_role_to_rule_entries) | **GET** /v2/applications/{app_id}/role_to_rule_entries | Get all RoleToRuleEntries
[**list_roles**](ApplicationsApi.md#list_roles) | **GET** /v2/applications/{app_id}/roles | Get all roles
[**list_rules**](ApplicationsApi.md#list_rules) | **GET** /v2/applications/{app_id}/rules | Get all rules
[**list_runtime_status**](ApplicationsApi.md#list_runtime_status) | **GET** /v2/applications/{app_id}/environments/{env_name}/status/runtime_status | Get an environment&#39;s runtime status
[**replace_agent**](ApplicationsApi.md#replace_agent) | **PUT** /v2/secure_agents/{agent_id} | Update a secure agent
[**replace_application**](ApplicationsApi.md#replace_application) | **PUT** /v2/applications/{app_id} | Create or update an application
[**replace_config**](ApplicationsApi.md#replace_config) | **PUT** /v2/applications/{app_id}/environments/{env_name}/configs/{env_config_id} | Update environment configuration
[**replace_environment**](ApplicationsApi.md#replace_environment) | **PUT** /v2/applications/{app_id}/environments/{env_name} | Update an environment
[**replace_role**](ApplicationsApi.md#replace_role) | **PUT** /v2/applications/{app_id}/roles/{role_id} | Update a role
[**replace_role_to_rule_entry**](ApplicationsApi.md#replace_role_to_rule_entry) | **PUT** /v2/applications/{app_id}/role_to_rule_entries/{role_to_rule_entry_id} | Update a role_to_rule_entry
[**replace_rule**](ApplicationsApi.md#replace_rule) | **PUT** /v2/applications/{app_id}/rules/{rule_id} | Update a rule
[**replace_runtime_status**](ApplicationsApi.md#replace_runtime_status) | **PUT** /v2/applications/{app_id}/environments/{env_name}/status/runtime_status | update an environemnt&#39;s runtime status


# **add_config**
> EnvironmentConfig add_config(app_id, env_name, environment_config)

Add an environment configuration row

Add an environment configuration row

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
env_name = 'env_name_example' # str | The name of an Environment
environment_config = agilicus_api.EnvironmentConfig() # EnvironmentConfig | 

    try:
        # Add an environment configuration row
        api_response = api_instance.add_config(app_id, env_name, environment_config)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->add_config: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **env_name** | **str**| The name of an Environment | 
 **environment_config** | [**EnvironmentConfig**](EnvironmentConfig.md)|  | 

### Return type

[**EnvironmentConfig**](EnvironmentConfig.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New environment config row created |  -  |
**409** | Environment configuration requested already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_role**
> RoleV2 add_role(app_id, role_v2)

Add a role to the application.

Add a role to the application.

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
role_v2 = agilicus_api.RoleV2() # RoleV2 | 

    try:
        # Add a role to the application.
        api_response = api_instance.add_role(app_id, role_v2)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->add_role: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **role_v2** | [**RoleV2**](RoleV2.md)|  | 

### Return type

[**RoleV2**](RoleV2.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New role created |  -  |
**409** | A role of this name already exists in the application. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_role_to_rule_entry**
> RoleToRuleEntry add_role_to_rule_entry(app_id, role_to_rule_entry)

Add a rule to a role in the application.

Add a rule to a role in the application.

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
role_to_rule_entry = agilicus_api.RoleToRuleEntry() # RoleToRuleEntry | 

    try:
        # Add a rule to a role in the application.
        api_response = api_instance.add_role_to_rule_entry(app_id, role_to_rule_entry)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->add_role_to_rule_entry: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **role_to_rule_entry** | [**RoleToRuleEntry**](RoleToRuleEntry.md)|  | 

### Return type

[**RoleToRuleEntry**](RoleToRuleEntry.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New role_to_rule_entry created |  -  |
**409** | The rule is already mapped to the role |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_rule**
> RuleV2 add_rule(app_id, rule_v2)

Add a rule to the application.

Add a rule to the application.

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
rule_v2 = agilicus_api.RuleV2() # RuleV2 | 

    try:
        # Add a rule to the application.
        api_response = api_instance.add_rule(app_id, rule_v2)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->add_rule: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **rule_v2** | [**RuleV2**](RuleV2.md)|  | 

### Return type

[**RuleV2**](RuleV2.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New rule created |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_agent**
> SecureAgent create_agent(secure_agent)

Create a secure agent

Create a secure agent

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    secure_agent = agilicus_api.SecureAgent() # SecureAgent | 

    try:
        # Create a secure agent
        api_response = api_instance.create_agent(secure_agent)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->create_agent: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **secure_agent** | [**SecureAgent**](SecureAgent.md)|  | 

### Return type

[**SecureAgent**](SecureAgent.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New secure agent |  -  |
**400** | The contents of the request body are invalid |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_application**
> Application create_application(application)

Create an application

Create an application according to spec

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    application = agilicus_api.Application() # Application | 

    try:
        # Create an application
        api_response = api_instance.create_application(application)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->create_application: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **application** | [**Application**](Application.md)|  | 

### Return type

[**Application**](Application.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New application created |  -  |
**409** | Application already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_agent**
> delete_agent(agent_id, org_id=org_id)

Delete a secure agent

Delete a secure agent

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    agent_id = '1234' # str | agent id path
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Delete a secure agent
        api_instance.delete_agent(agent_id, org_id=org_id)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->delete_agent: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **agent_id** | **str**| agent id path | 
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
**204** | secure agent was deleted |  -  |
**404** | secure agent does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_application**
> delete_application(app_id, org_id=org_id)

Remove an application

Remove an application

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Remove an application
        api_instance.delete_application(app_id, org_id=org_id)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->delete_application: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
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
**204** | Application was deleted |  -  |
**404** | Application does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_config**
> delete_config(app_id, env_name, env_config_id, maintenance_org_id)

Remove an environment configuration

Remove an environment configuration

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
env_name = 'env_name_example' # str | The name of an Environment
env_config_id = 'env_config_id_example' # str | environment configuration id
maintenance_org_id = 'maintenance_org_id_example' # str | Organisation unique identifier for an object being maintained by an organisation different than it. 

    try:
        # Remove an environment configuration
        api_instance.delete_config(app_id, env_name, env_config_id, maintenance_org_id)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->delete_config: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **env_name** | **str**| The name of an Environment | 
 **env_config_id** | **str**| environment configuration id | 
 **maintenance_org_id** | **str**| Organisation unique identifier for an object being maintained by an organisation different than it.  | 

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
**204** | Environment configuration was deleted |  -  |
**404** | Environment configuration does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_role**
> delete_role(app_id, role_id, org_id=org_id)

Remove a role

Remove a role

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
role_id = 'Absadal2' # str | The id of a role
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Remove a role
        api_instance.delete_role(app_id, role_id, org_id=org_id)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->delete_role: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **role_id** | **str**| The id of a role | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Role was deleted |  -  |
**404** | The Role does not exist. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_role_to_rule_entry**
> delete_role_to_rule_entry(app_id, role_to_rule_entry_id, org_id=org_id)

Remove a role_to_rule_entry

Remove a role_to_rule_entry

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
role_to_rule_entry_id = 'Absadal2' # str | The id of a role to rule entry
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Remove a role_to_rule_entry
        api_instance.delete_role_to_rule_entry(app_id, role_to_rule_entry_id, org_id=org_id)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->delete_role_to_rule_entry: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **role_to_rule_entry_id** | **str**| The id of a role to rule entry | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | RoleToRuleEntry was deleted |  -  |
**404** | The RoleToRuleEntry does not exist. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_rule**
> delete_rule(app_id, rule_id, org_id=org_id)

Remove a rule

Remove a rule

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
rule_id = 'Absadal2' # str | The id of a rule
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Remove a rule
        api_instance.delete_rule(app_id, rule_id, org_id=org_id)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->delete_rule: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **rule_id** | **str**| The id of a rule | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Rule was deleted |  -  |
**404** | The Rule does not exist. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_agent**
> SecureAgent get_agent(agent_id, org_id=org_id)

Get a secure agent

Get a secure agent

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    agent_id = '1234' # str | agent id path
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Get a secure agent
        api_response = api_instance.get_agent(agent_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->get_agent: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **agent_id** | **str**| agent id path | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**SecureAgent**](SecureAgent.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | secure agent found and returned |  -  |
**404** | secure agent does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_application**
> Application get_application(app_id, org_id=org_id, assigned_org_id=assigned_org_id)

Get a application

Get a application

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
org_id = '1234' # str | Organisation Unique identifier (optional)
assigned_org_id = 'assigned_org_id_example' # str | Organisation unique identifier for an assigned object (optional)

    try:
        # Get a application
        api_response = api_instance.get_application(app_id, org_id=org_id, assigned_org_id=assigned_org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->get_application: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **assigned_org_id** | **str**| Organisation unique identifier for an assigned object | [optional] 

### Return type

[**Application**](Application.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return Application |  -  |
**404** | Application does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_config**
> EnvironmentConfig get_config(app_id, env_name, env_config_id, maintenance_org_id)

Get environment configuration

Retrieve environment configuration 

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
env_name = 'env_name_example' # str | The name of an Environment
env_config_id = 'env_config_id_example' # str | environment configuration id
maintenance_org_id = 'maintenance_org_id_example' # str | Organisation unique identifier for an object being maintained by an organisation different than it. 

    try:
        # Get environment configuration
        api_response = api_instance.get_config(app_id, env_name, env_config_id, maintenance_org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->get_config: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **env_name** | **str**| The name of an Environment | 
 **env_config_id** | **str**| environment configuration id | 
 **maintenance_org_id** | **str**| Organisation unique identifier for an object being maintained by an organisation different than it.  | 

### Return type

[**EnvironmentConfig**](EnvironmentConfig.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Environment configuration successfully retrieved. |  -  |
**403** | Reading this environment is not permitted. This could happen due to insufficient permissions within your organisation.  |  -  |
**404** | The Environment configuration does not exist. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_environment**
> Environment get_environment(app_id, env_name, org_id)

Get an environment

This allows an environment maintainer to get an environment they maintain. 

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
env_name = 'env_name_example' # str | The name of an Environment
org_id = 'org_id_example' # str | Organisation unique identifier

    try:
        # Get an environment
        api_response = api_instance.get_environment(app_id, env_name, org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->get_environment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **env_name** | **str**| The name of an Environment | 
 **org_id** | **str**| Organisation unique identifier | 

### Return type

[**Environment**](Environment.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Environment successfully retrieved. |  -  |
**403** | Reading this environment is not permitted. This could happen due to insufficient permissions within your organisation.  |  -  |
**404** | Environment does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_role**
> RoleV2 get_role(app_id, role_id, org_id=org_id)

Get a role

Retrieves a given role by ID 

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
role_id = 'Absadal2' # str | The id of a role
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Get a role
        api_response = api_instance.get_role(app_id, role_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->get_role: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **role_id** | **str**| The id of a role | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**RoleV2**](RoleV2.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Role successfully retrieved. |  -  |
**404** | Role does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_role_to_rule_entry**
> RoleToRuleEntry get_role_to_rule_entry(app_id, role_to_rule_entry_id, org_id=org_id)

Get a role_to_rule_entry

Retrieves a given role_to_rule_entry by ID 

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
role_to_rule_entry_id = 'Absadal2' # str | The id of a role to rule entry
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Get a role_to_rule_entry
        api_response = api_instance.get_role_to_rule_entry(app_id, role_to_rule_entry_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->get_role_to_rule_entry: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **role_to_rule_entry_id** | **str**| The id of a role to rule entry | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**RoleToRuleEntry**](RoleToRuleEntry.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | RoleToRuleEntry successfully retrieved. |  -  |
**404** | RoleToRuleEntry does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_rule**
> RuleV2 get_rule(app_id, rule_id, org_id=org_id)

Get a rule

Retrieves a given rule by ID 

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
rule_id = 'Absadal2' # str | The id of a rule
org_id = '1234' # str | Organisation Unique identifier (optional)

    try:
        # Get a rule
        api_response = api_instance.get_rule(app_id, rule_id, org_id=org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->get_rule: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **rule_id** | **str**| The id of a rule | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 

### Return type

[**RuleV2**](RuleV2.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Rule successfully retrieved. |  -  |
**404** | Rule does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_agents**
> ListSecureAgentResponse list_agents(limit=limit, org_id=org_id, name=name)

List secure agents

List secure agents

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
org_id = '1234' # str | Organisation Unique identifier (optional)
name = 'host1_agent' # str | Query the agents by name (optional)

    try:
        # List secure agents
        api_response = api_instance.list_agents(limit=limit, org_id=org_id, name=name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->list_agents: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **name** | **str**| Query the agents by name | [optional] 

### Return type

[**ListSecureAgentResponse**](ListSecureAgentResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return a list of secure agents |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_application_summaries**
> ListApplicationSummaryResponse list_application_summaries(org_id=org_id, assigned_org_ids=assigned_org_ids, limit=limit)

List application summaries

Retrieve all application summaries corresponding to the provided parameters. One summary will exist per organisation assigned to the application. If a single org id is provided in the `org_id` parameter, then all assignments for all applications owned by that org will be listed. If a list of org ids are provided via the `assigned_org_ids` parameter, then the assignments will be constrained to ones for those org ids. Note that these two org id parameters can work together. One constrains the applications, and the other the assignments, so the combination of the two could be used to show a subset of the assignments for a given organisation's applications. 

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    org_id = '1234' # str | Organisation Unique identifier (optional)
assigned_org_ids = ['[\"q20sd0dfs3llasd0af9\"]'] # list[str] | The asssigned org ids to search for. Each org will be searched for independently. (optional)
limit = 500 # int | limit the number of rows in the response (optional) (default to 500)

    try:
        # List application summaries
        api_response = api_instance.list_application_summaries(org_id=org_id, assigned_org_ids=assigned_org_ids, limit=limit)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->list_application_summaries: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **assigned_org_ids** | [**list[str]**](str.md)| The asssigned org ids to search for. Each org will be searched for independently. | [optional] 
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]

### Return type

[**ListApplicationSummaryResponse**](ListApplicationSummaryResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | ApplicationSummary list successfully retrieved |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_applications**
> ListApplicationsResponse list_applications(org_id=org_id, assigned_org_id=assigned_org_id, maintained=maintained, assigned=assigned, owned=owned, updated_since=updated_since, show_status=show_status, application_type=application_type)

Get applications

Retrieves all applications related to the org_id. Different types of relationship may be queried by setting the appropriate flags:   - assigned: Has an Environment assigned to the organisation.   - owned: Owned by the organisation.   - maintained: Has an Environment maintained by the organisation. Any combination of the relationship flags may be set. Note that if the organisation does not own the Application, but maintains or is assigned an environment only those assignments and environments for the querying organisation will be shown. 

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    org_id = '1234' # str | Organisation Unique identifier (optional)
assigned_org_id = 'assigned_org_id_example' # str | Organisation unique identifier for an assigned object (optional)
maintained = True # bool | Query for Applications maintained by the `org_id`. These are Applications which have an Environment whose `maintenance_org_id` is the `org_id`.  (optional)
assigned = True # bool | Query for Applications assigned to the `org_id`. These are Applications with at least one Environment assigned to the `org_id`.  (optional)
owned = True # bool | Query for Applications owned by the `org_id`. (optional)
updated_since = '2015-07-07T15:49:51.230+02:00' # datetime | query since updated (optional)
show_status = False # bool | Whether the return value should include the status for included objects. If false the query may run faster but will not include status information.  (optional) (default to False)
application_type = ["user_defined"] # list[str] | Query based on the application type. Multiple values are ORed together.  (optional) (default to ["user_defined"])

    try:
        # Get applications
        api_response = api_instance.list_applications(org_id=org_id, assigned_org_id=assigned_org_id, maintained=maintained, assigned=assigned, owned=owned, updated_since=updated_since, show_status=show_status, application_type=application_type)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->list_applications: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **assigned_org_id** | **str**| Organisation unique identifier for an assigned object | [optional] 
 **maintained** | **bool**| Query for Applications maintained by the &#x60;org_id&#x60;. These are Applications which have an Environment whose &#x60;maintenance_org_id&#x60; is the &#x60;org_id&#x60;.  | [optional] 
 **assigned** | **bool**| Query for Applications assigned to the &#x60;org_id&#x60;. These are Applications with at least one Environment assigned to the &#x60;org_id&#x60;.  | [optional] 
 **owned** | **bool**| Query for Applications owned by the &#x60;org_id&#x60;. | [optional] 
 **updated_since** | **datetime**| query since updated | [optional] 
 **show_status** | **bool**| Whether the return value should include the status for included objects. If false the query may run faster but will not include status information.  | [optional] [default to False]
 **application_type** | [**list[str]**](str.md)| Query based on the application type. Multiple values are ORed together.  | [optional] [default to [&quot;user_defined&quot;]]

### Return type

[**ListApplicationsResponse**](ListApplicationsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Return applications |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_combined_rules**
> ListCombinedRulesResponse list_combined_rules(org_id=org_id, scopes=scopes, app_id=app_id, limit=limit, assigned=assigned)

List rules combined by scope or role

Retrieve all role_to_rule_entries for an application. If assigned is true, this will list all role_to_rule_entries for applications assigned to the given org_id 

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    org_id = '1234' # str | Organisation Unique identifier (optional)
scopes = [agilicus_api.RuleScopeEnum()] # list[RuleScopeEnum] | The scopes of the rules to search for. Multiple values are ORed together. (optional)
app_id = 'app_id_example' # str | Application unique identifier (optional)
limit = 500 # int | limit the number of rows in the response (optional) (default to 500)
assigned = True # bool | Query for Applications assigned to the `org_id`. These are Applications with at least one Environment assigned to the `org_id`.  (optional)

    try:
        # List rules combined by scope or role
        api_response = api_instance.list_combined_rules(org_id=org_id, scopes=scopes, app_id=app_id, limit=limit, assigned=assigned)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->list_combined_rules: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **scopes** | [**list[RuleScopeEnum]**](RuleScopeEnum.md)| The scopes of the rules to search for. Multiple values are ORed together. | [optional] 
 **app_id** | **str**| Application unique identifier | [optional] 
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]
 **assigned** | **bool**| Query for Applications assigned to the &#x60;org_id&#x60;. These are Applications with at least one Environment assigned to the &#x60;org_id&#x60;.  | [optional] 

### Return type

[**ListCombinedRulesResponse**](ListCombinedRulesResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | CombinedRules were successfully retrieved |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_configs**
> ListConfigsResponse list_configs(app_id, env_name, maintenance_org_id)

Get all environment configuration

Retrieve all environment configuration 

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
env_name = 'env_name_example' # str | The name of an Environment
maintenance_org_id = 'maintenance_org_id_example' # str | Organisation unique identifier for an object being maintained by an organisation different than it. 

    try:
        # Get all environment configuration
        api_response = api_instance.list_configs(app_id, env_name, maintenance_org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->list_configs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **env_name** | **str**| The name of an Environment | 
 **maintenance_org_id** | **str**| Organisation unique identifier for an object being maintained by an organisation different than it.  | 

### Return type

[**ListConfigsResponse**](ListConfigsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Environment configuration successfully retrieved. |  -  |
**403** | Reading this environment is not permitted. This could happen due to insufficient permissions within your organisation.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_environment_configs_all_apps**
> ListEnvironmentConfigsResponse list_environment_configs_all_apps(maintenance_org_id, limit=limit)

Get all environment configuration for a given organisation.

Retrieve all environment configuration for a organisation. 

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    maintenance_org_id = 'maintenance_org_id_example' # str | Organisation unique identifier for an object being maintained by an organisation different than it. 
limit = 500 # int | limit the number of rows in the response (optional) (default to 500)

    try:
        # Get all environment configuration for a given organisation.
        api_response = api_instance.list_environment_configs_all_apps(maintenance_org_id, limit=limit)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->list_environment_configs_all_apps: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **maintenance_org_id** | **str**| Organisation unique identifier for an object being maintained by an organisation different than it.  | 
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]

### Return type

[**ListEnvironmentConfigsResponse**](ListEnvironmentConfigsResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Environment configuration successfully retrieved. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_role_to_rule_entries**
> ListRoleToRuleEntries list_role_to_rule_entries(app_id, org_id=org_id, limit=limit)

Get all RoleToRuleEntries

Retrieve all role_to_rule_entries for an application 

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
org_id = '1234' # str | Organisation Unique identifier (optional)
limit = 500 # int | limit the number of rows in the response (optional) (default to 500)

    try:
        # Get all RoleToRuleEntries
        api_response = api_instance.list_role_to_rule_entries(app_id, org_id=org_id, limit=limit)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->list_role_to_rule_entries: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]

### Return type

[**ListRoleToRuleEntries**](ListRoleToRuleEntries.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | RoleToRuleEntries successfully retrieved. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_roles**
> ListRoles list_roles(app_id, org_id=org_id, limit=limit)

Get all roles

Retrieve all roles for an application 

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
org_id = '1234' # str | Organisation Unique identifier (optional)
limit = 500 # int | limit the number of rows in the response (optional) (default to 500)

    try:
        # Get all roles
        api_response = api_instance.list_roles(app_id, org_id=org_id, limit=limit)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->list_roles: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]

### Return type

[**ListRoles**](ListRoles.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Roles successfully retrieved. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_rules**
> ListRules list_rules(app_id, org_id=org_id, scope=scope, limit=limit)

Get all rules

Retrieve all rules for an application 

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
org_id = '1234' # str | Organisation Unique identifier (optional)
scope = agilicus_api.RuleScopeEnum() # RuleScopeEnum | The scope of the rules to search for (optional)
limit = 500 # int | limit the number of rows in the response (optional) (default to 500)

    try:
        # Get all rules
        api_response = api_instance.list_rules(app_id, org_id=org_id, scope=scope, limit=limit)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->list_rules: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **scope** | [**RuleScopeEnum**](.md)| The scope of the rules to search for | [optional] 
 **limit** | **int**| limit the number of rows in the response | [optional] [default to 500]

### Return type

[**ListRules**](ListRules.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Rules successfully retrieved. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_runtime_status**
> RuntimeStatus list_runtime_status(app_id, env_name, org_id)

Get an environment's runtime status

Get an environment's runtime status 

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
env_name = 'env_name_example' # str | The name of an Environment
org_id = 'org_id_example' # str | Organisation unique identifier

    try:
        # Get an environment's runtime status
        api_response = api_instance.list_runtime_status(app_id, env_name, org_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->list_runtime_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **env_name** | **str**| The name of an Environment | 
 **org_id** | **str**| Organisation unique identifier | 

### Return type

[**RuntimeStatus**](RuntimeStatus.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Environment status successfully retrieved. |  -  |
**403** | Reading this environment status is not permitted. This could happen due to insufficient permissions within your organisation.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_agent**
> SecureAgent replace_agent(agent_id, org_id=org_id, secure_agent=secure_agent)

Update a secure agent

Update a secure agent

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    agent_id = '1234' # str | agent id path
org_id = '1234' # str | Organisation Unique identifier (optional)
secure_agent = agilicus_api.SecureAgent() # SecureAgent |  (optional)

    try:
        # Update a secure agent
        api_response = api_instance.replace_agent(agent_id, org_id=org_id, secure_agent=secure_agent)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->replace_agent: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **agent_id** | **str**| agent id path | 
 **org_id** | **str**| Organisation Unique identifier | [optional] 
 **secure_agent** | [**SecureAgent**](SecureAgent.md)|  | [optional] 

### Return type

[**SecureAgent**](SecureAgent.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | secure agent updated |  -  |
**400** | The contents of the request body are invalid |  -  |
**404** | secure agent does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_application**
> Application replace_application(app_id, application=application)

Create or update an application

Create or update an application

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
application = agilicus_api.Application() # Application |  (optional)

    try:
        # Create or update an application
        api_response = api_instance.replace_application(app_id, application=application)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->replace_application: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **application** | [**Application**](Application.md)|  | [optional] 

### Return type

[**Application**](Application.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The Application was updated. Returns the latest version of it after applying the update.  |  -  |
**404** | Application does not exists |  -  |
**409** | The provided Application conflicted with the value stored in the API. Please fetch the latest version and try again with it.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_config**
> EnvironmentConfig replace_config(app_id, env_name, env_config_id, environment_config)

Update environment configuration

Update environment configuration 

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
env_name = 'env_name_example' # str | The name of an Environment
env_config_id = 'env_config_id_example' # str | environment configuration id
environment_config = agilicus_api.EnvironmentConfig() # EnvironmentConfig | 

    try:
        # Update environment configuration
        api_response = api_instance.replace_config(app_id, env_name, env_config_id, environment_config)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->replace_config: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **env_name** | **str**| The name of an Environment | 
 **env_config_id** | **str**| environment configuration id | 
 **environment_config** | [**EnvironmentConfig**](EnvironmentConfig.md)|  | 

### Return type

[**EnvironmentConfig**](EnvironmentConfig.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The Environment configuration was successfully updated |  -  |
**403** | Reading this environment is not permitted. This could happen due to insufficient permissions within your organisation.  |  -  |
**404** | The Environment configuration does not exist. |  -  |
**409** | The provided Environment Configuration conflicted with the value stored in the API. Please fetch the latest version and try again with it.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_environment**
> Environment replace_environment(app_id, env_name, environment=environment)

Update an environment

This allows an environment maintainer to update the environment. Note that the maintenence_organisation in the body must match the existing one. 

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
env_name = 'env_name_example' # str | The name of an Environment
environment = agilicus_api.Environment() # Environment |  (optional)

    try:
        # Update an environment
        api_response = api_instance.replace_environment(app_id, env_name, environment=environment)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->replace_environment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **env_name** | **str**| The name of an Environment | 
 **environment** | [**Environment**](Environment.md)|  | [optional] 

### Return type

[**Environment**](Environment.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The Environment was updated. Returns the latest version of it after the update was applied.  |  -  |
**403** | Modifying this environment is not permitted. This could happen due to insufficient permissions within your organisation, or because you tried to change the maintenence organisation of an environment.  |  -  |
**404** | The Environment does not exist. |  -  |
**409** | The provided Environment conflicted with the value stored in the API. Please fetch the latest version and try again with it.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_role**
> RoleV2 replace_role(app_id, role_id, role_v2=role_v2)

Update a role

Updates a role with a new specification. 

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
role_id = 'Absadal2' # str | The id of a role
role_v2 = agilicus_api.RoleV2() # RoleV2 |  (optional)

    try:
        # Update a role
        api_response = api_instance.replace_role(app_id, role_id, role_v2=role_v2)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->replace_role: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **role_id** | **str**| The id of a role | 
 **role_v2** | [**RoleV2**](RoleV2.md)|  | [optional] 

### Return type

[**RoleV2**](RoleV2.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The Role was updated. Returns the latest version of it after the update was applied.  |  -  |
**404** | The Role does not exist. |  -  |
**409** | The provided Role conflicted with the value stored in the API. Please fetch the latest version and try again with it.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_role_to_rule_entry**
> RoleToRuleEntry replace_role_to_rule_entry(app_id, role_to_rule_entry_id, role_to_rule_entry=role_to_rule_entry)

Update a role_to_rule_entry

Updates a role_to_rule_entry with a new specification. 

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
role_to_rule_entry_id = 'Absadal2' # str | The id of a role to rule entry
role_to_rule_entry = agilicus_api.RoleToRuleEntry() # RoleToRuleEntry |  (optional)

    try:
        # Update a role_to_rule_entry
        api_response = api_instance.replace_role_to_rule_entry(app_id, role_to_rule_entry_id, role_to_rule_entry=role_to_rule_entry)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->replace_role_to_rule_entry: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **role_to_rule_entry_id** | **str**| The id of a role to rule entry | 
 **role_to_rule_entry** | [**RoleToRuleEntry**](RoleToRuleEntry.md)|  | [optional] 

### Return type

[**RoleToRuleEntry**](RoleToRuleEntry.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The RoleToRuleEntry was updated. Returns the latest version of it after the update was applied.  |  -  |
**404** | The RoleToRuleEntry does not exist. |  -  |
**409** | The provided RoleToRuleEntry conflicted with the value stored in the API. Please fetch the latest version and try again with it.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_rule**
> RuleV2 replace_rule(app_id, rule_id, rule_v2=rule_v2)

Update a rule

Updates a rule with a new specification. 

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
rule_id = 'Absadal2' # str | The id of a rule
rule_v2 = agilicus_api.RuleV2() # RuleV2 |  (optional)

    try:
        # Update a rule
        api_response = api_instance.replace_rule(app_id, rule_id, rule_v2=rule_v2)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->replace_rule: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **rule_id** | **str**| The id of a rule | 
 **rule_v2** | [**RuleV2**](RuleV2.md)|  | [optional] 

### Return type

[**RuleV2**](RuleV2.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The Rule was updated. Returns the latest version of it after the update was applied.  |  -  |
**404** | The Rule does not exist. |  -  |
**409** | The provided Rule conflicted with the value stored in the API. Please fetch the latest version and try again with it.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_runtime_status**
> RuntimeStatus replace_runtime_status(app_id, env_name, runtime_status)

update an environemnt's runtime status

update an environemnt's runtime status

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
    api_instance = agilicus_api.ApplicationsApi(api_client)
    app_id = 'app_id_example' # str | Application unique identifier
env_name = 'env_name_example' # str | The name of an Environment
runtime_status = agilicus_api.RuntimeStatus() # RuntimeStatus | 

    try:
        # update an environemnt's runtime status
        api_response = api_instance.replace_runtime_status(app_id, env_name, runtime_status)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ApplicationsApi->replace_runtime_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| Application unique identifier | 
 **env_name** | **str**| The name of an Environment | 
 **runtime_status** | [**RuntimeStatus**](RuntimeStatus.md)|  | 

### Return type

[**RuntimeStatus**](RuntimeStatus.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Update the environment&#39;s runtime status |  -  |
**403** | Changing the environment status is not permitted.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

