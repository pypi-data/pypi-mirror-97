# swagger_client.InternalApi

All URIs are relative to *https://api.curia.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**code_controller_get_upload_url**](InternalApi.md#code_controller_get_upload_url) | **GET** /codes/url | 
[**create_many_base_code_controller_code**](InternalApi.md#create_many_base_code_controller_code) | **POST** /codes/bulk | Create many Code
[**create_many_base_feature_category_controller_feature_category**](InternalApi.md#create_many_base_feature_category_controller_feature_category) | **POST** /feature-categories/bulk | Create many FeatureCategory
[**create_many_base_feature_controller_feature**](InternalApi.md#create_many_base_feature_controller_feature) | **POST** /features/bulk | Create many Feature
[**create_many_base_feature_sub_category_controller_feature_sub_category**](InternalApi.md#create_many_base_feature_sub_category_controller_feature_sub_category) | **POST** /feature-sub-categories/bulk | Create many FeatureSubCategory
[**create_one_base_code_controller_code**](InternalApi.md#create_one_base_code_controller_code) | **POST** /codes | Create one Code
[**create_one_base_feature_category_controller_feature_category**](InternalApi.md#create_one_base_feature_category_controller_feature_category) | **POST** /feature-categories | Create one FeatureCategory
[**create_one_base_feature_controller_feature**](InternalApi.md#create_one_base_feature_controller_feature) | **POST** /features | Create one Feature
[**create_one_base_feature_sub_category_controller_feature_sub_category**](InternalApi.md#create_one_base_feature_sub_category_controller_feature_sub_category) | **POST** /feature-sub-categories | Create one FeatureSubCategory
[**delete_one_base_code_controller_code**](InternalApi.md#delete_one_base_code_controller_code) | **DELETE** /codes/{id} | Delete one Code
[**delete_one_base_feature_category_controller_feature_category**](InternalApi.md#delete_one_base_feature_category_controller_feature_category) | **DELETE** /feature-categories/{id} | Delete one FeatureCategory
[**delete_one_base_feature_controller_feature**](InternalApi.md#delete_one_base_feature_controller_feature) | **DELETE** /features/{id} | Delete one Feature
[**delete_one_base_feature_sub_category_controller_feature_sub_category**](InternalApi.md#delete_one_base_feature_sub_category_controller_feature_sub_category) | **DELETE** /feature-sub-categories/{id} | Delete one FeatureSubCategory
[**get_many_base_code_controller_code**](InternalApi.md#get_many_base_code_controller_code) | **GET** /codes | Retrieve many Code
[**get_many_base_feature_category_controller_feature_category**](InternalApi.md#get_many_base_feature_category_controller_feature_category) | **GET** /feature-categories | Retrieve many FeatureCategory
[**get_many_base_feature_controller_feature**](InternalApi.md#get_many_base_feature_controller_feature) | **GET** /features | Retrieve many Feature
[**get_many_base_feature_sub_category_controller_feature_sub_category**](InternalApi.md#get_many_base_feature_sub_category_controller_feature_sub_category) | **GET** /feature-sub-categories | Retrieve many FeatureSubCategory
[**get_one_base_code_controller_code**](InternalApi.md#get_one_base_code_controller_code) | **GET** /codes/{id} | Retrieve one Code
[**get_one_base_feature_category_controller_feature_category**](InternalApi.md#get_one_base_feature_category_controller_feature_category) | **GET** /feature-categories/{id} | Retrieve one FeatureCategory
[**get_one_base_feature_controller_feature**](InternalApi.md#get_one_base_feature_controller_feature) | **GET** /features/{id} | Retrieve one Feature
[**get_one_base_feature_sub_category_controller_feature_sub_category**](InternalApi.md#get_one_base_feature_sub_category_controller_feature_sub_category) | **GET** /feature-sub-categories/{id} | Retrieve one FeatureSubCategory
[**health_controller_health**](InternalApi.md#health_controller_health) | **GET** /health | 
[**organization_setting_controller_get_unscoped_organziation_settings**](InternalApi.md#organization_setting_controller_get_unscoped_organziation_settings) | **GET** /organization-settings/unscoped | 
[**replace_one_base_code_controller_code**](InternalApi.md#replace_one_base_code_controller_code) | **PUT** /codes/{id} | Replace one Code
[**replace_one_base_feature_category_controller_feature_category**](InternalApi.md#replace_one_base_feature_category_controller_feature_category) | **PUT** /feature-categories/{id} | Replace one FeatureCategory
[**replace_one_base_feature_controller_feature**](InternalApi.md#replace_one_base_feature_controller_feature) | **PUT** /features/{id} | Replace one Feature
[**replace_one_base_feature_sub_category_controller_feature_sub_category**](InternalApi.md#replace_one_base_feature_sub_category_controller_feature_sub_category) | **PUT** /feature-sub-categories/{id} | Replace one FeatureSubCategory
[**sns_message_controller_handle_message**](InternalApi.md#sns_message_controller_handle_message) | **POST** /sns-message | 
[**sns_message_controller_handle_message_0**](InternalApi.md#sns_message_controller_handle_message_0) | **POST** /sns-message | 
[**update_one_base_code_controller_code**](InternalApi.md#update_one_base_code_controller_code) | **PATCH** /codes/{id} | Update one Code
[**update_one_base_feature_category_controller_feature_category**](InternalApi.md#update_one_base_feature_category_controller_feature_category) | **PATCH** /feature-categories/{id} | Update one FeatureCategory
[**update_one_base_feature_controller_feature**](InternalApi.md#update_one_base_feature_controller_feature) | **PATCH** /features/{id} | Update one Feature
[**update_one_base_feature_sub_category_controller_feature_sub_category**](InternalApi.md#update_one_base_feature_sub_category_controller_feature_sub_category) | **PATCH** /feature-sub-categories/{id} | Update one FeatureSubCategory

# **code_controller_get_upload_url**
> code_controller_get_upload_url()



### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.InternalApi(swagger_client.ApiClient(configuration))

try:
    api_instance.code_controller_get_upload_url()
except ApiException as e:
    print("Exception when calling InternalApi->code_controller_get_upload_url: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_many_base_code_controller_code**
> list[Code] create_many_base_code_controller_code(body)

Create many Code

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.InternalApi(swagger_client.ApiClient(configuration))
body = swagger_client.CreateManyCodeDto() # CreateManyCodeDto | 

try:
    # Create many Code
    api_response = api_instance.create_many_base_code_controller_code(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InternalApi->create_many_base_code_controller_code: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateManyCodeDto**](CreateManyCodeDto.md)|  | 

### Return type

[**list[Code]**](Code.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_many_base_feature_category_controller_feature_category**
> list[FeatureCategory] create_many_base_feature_category_controller_feature_category(body)

Create many FeatureCategory

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.InternalApi(swagger_client.ApiClient(configuration))
body = swagger_client.CreateManyFeatureCategoryDto() # CreateManyFeatureCategoryDto | 

try:
    # Create many FeatureCategory
    api_response = api_instance.create_many_base_feature_category_controller_feature_category(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InternalApi->create_many_base_feature_category_controller_feature_category: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateManyFeatureCategoryDto**](CreateManyFeatureCategoryDto.md)|  | 

### Return type

[**list[FeatureCategory]**](FeatureCategory.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_many_base_feature_controller_feature**
> list[Feature] create_many_base_feature_controller_feature(body)

Create many Feature

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.InternalApi(swagger_client.ApiClient(configuration))
body = swagger_client.CreateManyFeatureDto() # CreateManyFeatureDto | 

try:
    # Create many Feature
    api_response = api_instance.create_many_base_feature_controller_feature(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InternalApi->create_many_base_feature_controller_feature: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateManyFeatureDto**](CreateManyFeatureDto.md)|  | 

### Return type

[**list[Feature]**](Feature.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_many_base_feature_sub_category_controller_feature_sub_category**
> list[FeatureSubCategory] create_many_base_feature_sub_category_controller_feature_sub_category(body)

Create many FeatureSubCategory

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.InternalApi(swagger_client.ApiClient(configuration))
body = swagger_client.CreateManyFeatureSubCategoryDto() # CreateManyFeatureSubCategoryDto | 

try:
    # Create many FeatureSubCategory
    api_response = api_instance.create_many_base_feature_sub_category_controller_feature_sub_category(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InternalApi->create_many_base_feature_sub_category_controller_feature_sub_category: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateManyFeatureSubCategoryDto**](CreateManyFeatureSubCategoryDto.md)|  | 

### Return type

[**list[FeatureSubCategory]**](FeatureSubCategory.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_one_base_code_controller_code**
> Code create_one_base_code_controller_code(body)

Create one Code

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.InternalApi(swagger_client.ApiClient(configuration))
body = swagger_client.Code() # Code | 

try:
    # Create one Code
    api_response = api_instance.create_one_base_code_controller_code(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InternalApi->create_one_base_code_controller_code: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Code**](Code.md)|  | 

### Return type

[**Code**](Code.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_one_base_feature_category_controller_feature_category**
> FeatureCategory create_one_base_feature_category_controller_feature_category(body)

Create one FeatureCategory

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.InternalApi(swagger_client.ApiClient(configuration))
body = swagger_client.FeatureCategory() # FeatureCategory | 

try:
    # Create one FeatureCategory
    api_response = api_instance.create_one_base_feature_category_controller_feature_category(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InternalApi->create_one_base_feature_category_controller_feature_category: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FeatureCategory**](FeatureCategory.md)|  | 

### Return type

[**FeatureCategory**](FeatureCategory.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_one_base_feature_controller_feature**
> Feature create_one_base_feature_controller_feature(body)

Create one Feature

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.InternalApi(swagger_client.ApiClient(configuration))
body = swagger_client.Feature() # Feature | 

try:
    # Create one Feature
    api_response = api_instance.create_one_base_feature_controller_feature(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InternalApi->create_one_base_feature_controller_feature: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Feature**](Feature.md)|  | 

### Return type

[**Feature**](Feature.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_one_base_feature_sub_category_controller_feature_sub_category**
> FeatureSubCategory create_one_base_feature_sub_category_controller_feature_sub_category(body)

Create one FeatureSubCategory

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.InternalApi(swagger_client.ApiClient(configuration))
body = swagger_client.FeatureSubCategory() # FeatureSubCategory | 

try:
    # Create one FeatureSubCategory
    api_response = api_instance.create_one_base_feature_sub_category_controller_feature_sub_category(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InternalApi->create_one_base_feature_sub_category_controller_feature_sub_category: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FeatureSubCategory**](FeatureSubCategory.md)|  | 

### Return type

[**FeatureSubCategory**](FeatureSubCategory.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_one_base_code_controller_code**
> delete_one_base_code_controller_code(id)

Delete one Code

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.InternalApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Delete one Code
    api_instance.delete_one_base_code_controller_code(id)
except ApiException as e:
    print("Exception when calling InternalApi->delete_one_base_code_controller_code: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_one_base_feature_category_controller_feature_category**
> delete_one_base_feature_category_controller_feature_category(id)

Delete one FeatureCategory

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.InternalApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Delete one FeatureCategory
    api_instance.delete_one_base_feature_category_controller_feature_category(id)
except ApiException as e:
    print("Exception when calling InternalApi->delete_one_base_feature_category_controller_feature_category: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_one_base_feature_controller_feature**
> delete_one_base_feature_controller_feature(id)

Delete one Feature

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.InternalApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Delete one Feature
    api_instance.delete_one_base_feature_controller_feature(id)
except ApiException as e:
    print("Exception when calling InternalApi->delete_one_base_feature_controller_feature: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_one_base_feature_sub_category_controller_feature_sub_category**
> delete_one_base_feature_sub_category_controller_feature_sub_category(id)

Delete one FeatureSubCategory

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.InternalApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Delete one FeatureSubCategory
    api_instance.delete_one_base_feature_sub_category_controller_feature_sub_category(id)
except ApiException as e:
    print("Exception when calling InternalApi->delete_one_base_feature_sub_category_controller_feature_sub_category: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_many_base_code_controller_code**
> GetManyCodeResponseDto get_many_base_code_controller_code(fields=fields, s=s, filter=filter, _or=_or, sort=sort, join=join, limit=limit, offset=offset, page=page, cache=cache)

Retrieve many Code

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.InternalApi(swagger_client.ApiClient(configuration))
fields = ['fields_example'] # list[str] | Selects resource fields. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#select\" target=\"_blank\">Docs</a> (optional)
s = 's_example' # str | Adds search condition. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#search\" target=\"_blank\">Docs</a> (optional)
filter = ['filter_example'] # list[str] | Adds filter condition. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#filter\" target=\"_blank\">Docs</a> (optional)
_or = ['_or_example'] # list[str] | Adds OR condition. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#or\" target=\"_blank\">Docs</a> (optional)
sort = ['sort_example'] # list[str] | Adds sort by field. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#sort\" target=\"_blank\">Docs</a> (optional)
join = ['join_example'] # list[str] | Adds relational resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#join\" target=\"_blank\">Docs</a> (optional)
limit = 56 # int | Limit amount of resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#limit\" target=\"_blank\">Docs</a> (optional)
offset = 56 # int | Offset amount of resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#offset\" target=\"_blank\">Docs</a> (optional)
page = 56 # int | Page portion of resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#page\" target=\"_blank\">Docs</a> (optional)
cache = 56 # int | Reset cache (if was enabled). <a href=\"https://github.com/nestjsx/crud/wiki/Requests#cache\" target=\"_blank\">Docs</a> (optional)

try:
    # Retrieve many Code
    api_response = api_instance.get_many_base_code_controller_code(fields=fields, s=s, filter=filter, _or=_or, sort=sort, join=join, limit=limit, offset=offset, page=page, cache=cache)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InternalApi->get_many_base_code_controller_code: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fields** | [**list[str]**](str.md)| Selects resource fields. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#select\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **s** | **str**| Adds search condition. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#search\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **filter** | [**list[str]**](str.md)| Adds filter condition. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#filter\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **_or** | [**list[str]**](str.md)| Adds OR condition. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#or\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **sort** | [**list[str]**](str.md)| Adds sort by field. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#sort\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **join** | [**list[str]**](str.md)| Adds relational resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#join\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **limit** | **int**| Limit amount of resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#limit\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **offset** | **int**| Offset amount of resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#offset\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **page** | **int**| Page portion of resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#page\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **cache** | **int**| Reset cache (if was enabled). &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#cache\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 

### Return type

[**GetManyCodeResponseDto**](GetManyCodeResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_many_base_feature_category_controller_feature_category**
> GetManyFeatureCategoryResponseDto get_many_base_feature_category_controller_feature_category(fields=fields, s=s, filter=filter, _or=_or, sort=sort, join=join, limit=limit, offset=offset, page=page, cache=cache)

Retrieve many FeatureCategory

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.InternalApi(swagger_client.ApiClient(configuration))
fields = ['fields_example'] # list[str] | Selects resource fields. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#select\" target=\"_blank\">Docs</a> (optional)
s = 's_example' # str | Adds search condition. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#search\" target=\"_blank\">Docs</a> (optional)
filter = ['filter_example'] # list[str] | Adds filter condition. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#filter\" target=\"_blank\">Docs</a> (optional)
_or = ['_or_example'] # list[str] | Adds OR condition. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#or\" target=\"_blank\">Docs</a> (optional)
sort = ['sort_example'] # list[str] | Adds sort by field. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#sort\" target=\"_blank\">Docs</a> (optional)
join = ['join_example'] # list[str] | Adds relational resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#join\" target=\"_blank\">Docs</a> (optional)
limit = 56 # int | Limit amount of resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#limit\" target=\"_blank\">Docs</a> (optional)
offset = 56 # int | Offset amount of resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#offset\" target=\"_blank\">Docs</a> (optional)
page = 56 # int | Page portion of resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#page\" target=\"_blank\">Docs</a> (optional)
cache = 56 # int | Reset cache (if was enabled). <a href=\"https://github.com/nestjsx/crud/wiki/Requests#cache\" target=\"_blank\">Docs</a> (optional)

try:
    # Retrieve many FeatureCategory
    api_response = api_instance.get_many_base_feature_category_controller_feature_category(fields=fields, s=s, filter=filter, _or=_or, sort=sort, join=join, limit=limit, offset=offset, page=page, cache=cache)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InternalApi->get_many_base_feature_category_controller_feature_category: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fields** | [**list[str]**](str.md)| Selects resource fields. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#select\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **s** | **str**| Adds search condition. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#search\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **filter** | [**list[str]**](str.md)| Adds filter condition. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#filter\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **_or** | [**list[str]**](str.md)| Adds OR condition. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#or\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **sort** | [**list[str]**](str.md)| Adds sort by field. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#sort\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **join** | [**list[str]**](str.md)| Adds relational resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#join\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **limit** | **int**| Limit amount of resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#limit\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **offset** | **int**| Offset amount of resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#offset\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **page** | **int**| Page portion of resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#page\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **cache** | **int**| Reset cache (if was enabled). &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#cache\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 

### Return type

[**GetManyFeatureCategoryResponseDto**](GetManyFeatureCategoryResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_many_base_feature_controller_feature**
> GetManyFeatureResponseDto get_many_base_feature_controller_feature(fields=fields, s=s, filter=filter, _or=_or, sort=sort, join=join, limit=limit, offset=offset, page=page, cache=cache)

Retrieve many Feature

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.InternalApi(swagger_client.ApiClient(configuration))
fields = ['fields_example'] # list[str] | Selects resource fields. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#select\" target=\"_blank\">Docs</a> (optional)
s = 's_example' # str | Adds search condition. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#search\" target=\"_blank\">Docs</a> (optional)
filter = ['filter_example'] # list[str] | Adds filter condition. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#filter\" target=\"_blank\">Docs</a> (optional)
_or = ['_or_example'] # list[str] | Adds OR condition. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#or\" target=\"_blank\">Docs</a> (optional)
sort = ['sort_example'] # list[str] | Adds sort by field. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#sort\" target=\"_blank\">Docs</a> (optional)
join = ['join_example'] # list[str] | Adds relational resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#join\" target=\"_blank\">Docs</a> (optional)
limit = 56 # int | Limit amount of resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#limit\" target=\"_blank\">Docs</a> (optional)
offset = 56 # int | Offset amount of resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#offset\" target=\"_blank\">Docs</a> (optional)
page = 56 # int | Page portion of resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#page\" target=\"_blank\">Docs</a> (optional)
cache = 56 # int | Reset cache (if was enabled). <a href=\"https://github.com/nestjsx/crud/wiki/Requests#cache\" target=\"_blank\">Docs</a> (optional)

try:
    # Retrieve many Feature
    api_response = api_instance.get_many_base_feature_controller_feature(fields=fields, s=s, filter=filter, _or=_or, sort=sort, join=join, limit=limit, offset=offset, page=page, cache=cache)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InternalApi->get_many_base_feature_controller_feature: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fields** | [**list[str]**](str.md)| Selects resource fields. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#select\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **s** | **str**| Adds search condition. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#search\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **filter** | [**list[str]**](str.md)| Adds filter condition. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#filter\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **_or** | [**list[str]**](str.md)| Adds OR condition. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#or\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **sort** | [**list[str]**](str.md)| Adds sort by field. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#sort\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **join** | [**list[str]**](str.md)| Adds relational resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#join\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **limit** | **int**| Limit amount of resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#limit\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **offset** | **int**| Offset amount of resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#offset\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **page** | **int**| Page portion of resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#page\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **cache** | **int**| Reset cache (if was enabled). &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#cache\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 

### Return type

[**GetManyFeatureResponseDto**](GetManyFeatureResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_many_base_feature_sub_category_controller_feature_sub_category**
> GetManyFeatureSubCategoryResponseDto get_many_base_feature_sub_category_controller_feature_sub_category(fields=fields, s=s, filter=filter, _or=_or, sort=sort, join=join, limit=limit, offset=offset, page=page, cache=cache)

Retrieve many FeatureSubCategory

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.InternalApi(swagger_client.ApiClient(configuration))
fields = ['fields_example'] # list[str] | Selects resource fields. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#select\" target=\"_blank\">Docs</a> (optional)
s = 's_example' # str | Adds search condition. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#search\" target=\"_blank\">Docs</a> (optional)
filter = ['filter_example'] # list[str] | Adds filter condition. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#filter\" target=\"_blank\">Docs</a> (optional)
_or = ['_or_example'] # list[str] | Adds OR condition. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#or\" target=\"_blank\">Docs</a> (optional)
sort = ['sort_example'] # list[str] | Adds sort by field. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#sort\" target=\"_blank\">Docs</a> (optional)
join = ['join_example'] # list[str] | Adds relational resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#join\" target=\"_blank\">Docs</a> (optional)
limit = 56 # int | Limit amount of resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#limit\" target=\"_blank\">Docs</a> (optional)
offset = 56 # int | Offset amount of resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#offset\" target=\"_blank\">Docs</a> (optional)
page = 56 # int | Page portion of resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#page\" target=\"_blank\">Docs</a> (optional)
cache = 56 # int | Reset cache (if was enabled). <a href=\"https://github.com/nestjsx/crud/wiki/Requests#cache\" target=\"_blank\">Docs</a> (optional)

try:
    # Retrieve many FeatureSubCategory
    api_response = api_instance.get_many_base_feature_sub_category_controller_feature_sub_category(fields=fields, s=s, filter=filter, _or=_or, sort=sort, join=join, limit=limit, offset=offset, page=page, cache=cache)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InternalApi->get_many_base_feature_sub_category_controller_feature_sub_category: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fields** | [**list[str]**](str.md)| Selects resource fields. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#select\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **s** | **str**| Adds search condition. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#search\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **filter** | [**list[str]**](str.md)| Adds filter condition. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#filter\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **_or** | [**list[str]**](str.md)| Adds OR condition. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#or\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **sort** | [**list[str]**](str.md)| Adds sort by field. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#sort\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **join** | [**list[str]**](str.md)| Adds relational resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#join\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **limit** | **int**| Limit amount of resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#limit\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **offset** | **int**| Offset amount of resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#offset\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **page** | **int**| Page portion of resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#page\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **cache** | **int**| Reset cache (if was enabled). &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#cache\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 

### Return type

[**GetManyFeatureSubCategoryResponseDto**](GetManyFeatureSubCategoryResponseDto.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_one_base_code_controller_code**
> Code get_one_base_code_controller_code(id, fields=fields, join=join, cache=cache)

Retrieve one Code

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.InternalApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 
fields = ['fields_example'] # list[str] | Selects resource fields. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#select\" target=\"_blank\">Docs</a> (optional)
join = ['join_example'] # list[str] | Adds relational resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#join\" target=\"_blank\">Docs</a> (optional)
cache = 56 # int | Reset cache (if was enabled). <a href=\"https://github.com/nestjsx/crud/wiki/Requests#cache\" target=\"_blank\">Docs</a> (optional)

try:
    # Retrieve one Code
    api_response = api_instance.get_one_base_code_controller_code(id, fields=fields, join=join, cache=cache)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InternalApi->get_one_base_code_controller_code: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **fields** | [**list[str]**](str.md)| Selects resource fields. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#select\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **join** | [**list[str]**](str.md)| Adds relational resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#join\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **cache** | **int**| Reset cache (if was enabled). &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#cache\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 

### Return type

[**Code**](Code.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_one_base_feature_category_controller_feature_category**
> FeatureCategory get_one_base_feature_category_controller_feature_category(id, fields=fields, join=join, cache=cache)

Retrieve one FeatureCategory

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.InternalApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 
fields = ['fields_example'] # list[str] | Selects resource fields. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#select\" target=\"_blank\">Docs</a> (optional)
join = ['join_example'] # list[str] | Adds relational resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#join\" target=\"_blank\">Docs</a> (optional)
cache = 56 # int | Reset cache (if was enabled). <a href=\"https://github.com/nestjsx/crud/wiki/Requests#cache\" target=\"_blank\">Docs</a> (optional)

try:
    # Retrieve one FeatureCategory
    api_response = api_instance.get_one_base_feature_category_controller_feature_category(id, fields=fields, join=join, cache=cache)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InternalApi->get_one_base_feature_category_controller_feature_category: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **fields** | [**list[str]**](str.md)| Selects resource fields. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#select\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **join** | [**list[str]**](str.md)| Adds relational resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#join\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **cache** | **int**| Reset cache (if was enabled). &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#cache\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 

### Return type

[**FeatureCategory**](FeatureCategory.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_one_base_feature_controller_feature**
> Feature get_one_base_feature_controller_feature(id, fields=fields, join=join, cache=cache)

Retrieve one Feature

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.InternalApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 
fields = ['fields_example'] # list[str] | Selects resource fields. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#select\" target=\"_blank\">Docs</a> (optional)
join = ['join_example'] # list[str] | Adds relational resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#join\" target=\"_blank\">Docs</a> (optional)
cache = 56 # int | Reset cache (if was enabled). <a href=\"https://github.com/nestjsx/crud/wiki/Requests#cache\" target=\"_blank\">Docs</a> (optional)

try:
    # Retrieve one Feature
    api_response = api_instance.get_one_base_feature_controller_feature(id, fields=fields, join=join, cache=cache)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InternalApi->get_one_base_feature_controller_feature: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **fields** | [**list[str]**](str.md)| Selects resource fields. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#select\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **join** | [**list[str]**](str.md)| Adds relational resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#join\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **cache** | **int**| Reset cache (if was enabled). &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#cache\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 

### Return type

[**Feature**](Feature.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_one_base_feature_sub_category_controller_feature_sub_category**
> FeatureSubCategory get_one_base_feature_sub_category_controller_feature_sub_category(id, fields=fields, join=join, cache=cache)

Retrieve one FeatureSubCategory

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.InternalApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 
fields = ['fields_example'] # list[str] | Selects resource fields. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#select\" target=\"_blank\">Docs</a> (optional)
join = ['join_example'] # list[str] | Adds relational resources. <a href=\"https://github.com/nestjsx/crud/wiki/Requests#join\" target=\"_blank\">Docs</a> (optional)
cache = 56 # int | Reset cache (if was enabled). <a href=\"https://github.com/nestjsx/crud/wiki/Requests#cache\" target=\"_blank\">Docs</a> (optional)

try:
    # Retrieve one FeatureSubCategory
    api_response = api_instance.get_one_base_feature_sub_category_controller_feature_sub_category(id, fields=fields, join=join, cache=cache)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InternalApi->get_one_base_feature_sub_category_controller_feature_sub_category: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **fields** | [**list[str]**](str.md)| Selects resource fields. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#select\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **join** | [**list[str]**](str.md)| Adds relational resources. &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#join\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 
 **cache** | **int**| Reset cache (if was enabled). &lt;a href&#x3D;\&quot;https://github.com/nestjsx/crud/wiki/Requests#cache\&quot; target&#x3D;\&quot;_blank\&quot;&gt;Docs&lt;/a&gt; | [optional] 

### Return type

[**FeatureSubCategory**](FeatureSubCategory.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **health_controller_health**
> health_controller_health()



### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.InternalApi()

try:
    api_instance.health_controller_health()
except ApiException as e:
    print("Exception when calling InternalApi->health_controller_health: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **organization_setting_controller_get_unscoped_organziation_settings**
> organization_setting_controller_get_unscoped_organziation_settings()



### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.InternalApi(swagger_client.ApiClient(configuration))

try:
    api_instance.organization_setting_controller_get_unscoped_organziation_settings()
except ApiException as e:
    print("Exception when calling InternalApi->organization_setting_controller_get_unscoped_organziation_settings: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_one_base_code_controller_code**
> Code replace_one_base_code_controller_code(body, id)

Replace one Code

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.InternalApi(swagger_client.ApiClient(configuration))
body = swagger_client.Code() # Code | 
id = 'id_example' # str | 

try:
    # Replace one Code
    api_response = api_instance.replace_one_base_code_controller_code(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InternalApi->replace_one_base_code_controller_code: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Code**](Code.md)|  | 
 **id** | **str**|  | 

### Return type

[**Code**](Code.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_one_base_feature_category_controller_feature_category**
> FeatureCategory replace_one_base_feature_category_controller_feature_category(body, id)

Replace one FeatureCategory

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.InternalApi(swagger_client.ApiClient(configuration))
body = swagger_client.FeatureCategory() # FeatureCategory | 
id = 'id_example' # str | 

try:
    # Replace one FeatureCategory
    api_response = api_instance.replace_one_base_feature_category_controller_feature_category(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InternalApi->replace_one_base_feature_category_controller_feature_category: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FeatureCategory**](FeatureCategory.md)|  | 
 **id** | **str**|  | 

### Return type

[**FeatureCategory**](FeatureCategory.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_one_base_feature_controller_feature**
> Feature replace_one_base_feature_controller_feature(body, id)

Replace one Feature

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.InternalApi(swagger_client.ApiClient(configuration))
body = swagger_client.Feature() # Feature | 
id = 'id_example' # str | 

try:
    # Replace one Feature
    api_response = api_instance.replace_one_base_feature_controller_feature(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InternalApi->replace_one_base_feature_controller_feature: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Feature**](Feature.md)|  | 
 **id** | **str**|  | 

### Return type

[**Feature**](Feature.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_one_base_feature_sub_category_controller_feature_sub_category**
> FeatureSubCategory replace_one_base_feature_sub_category_controller_feature_sub_category(body, id)

Replace one FeatureSubCategory

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.InternalApi(swagger_client.ApiClient(configuration))
body = swagger_client.FeatureSubCategory() # FeatureSubCategory | 
id = 'id_example' # str | 

try:
    # Replace one FeatureSubCategory
    api_response = api_instance.replace_one_base_feature_sub_category_controller_feature_sub_category(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InternalApi->replace_one_base_feature_sub_category_controller_feature_sub_category: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FeatureSubCategory**](FeatureSubCategory.md)|  | 
 **id** | **str**|  | 

### Return type

[**FeatureSubCategory**](FeatureSubCategory.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **sns_message_controller_handle_message**
> sns_message_controller_handle_message()



### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.InternalApi()

try:
    api_instance.sns_message_controller_handle_message()
except ApiException as e:
    print("Exception when calling InternalApi->sns_message_controller_handle_message: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **sns_message_controller_handle_message_0**
> sns_message_controller_handle_message_0()



### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.InternalApi()

try:
    api_instance.sns_message_controller_handle_message_0()
except ApiException as e:
    print("Exception when calling InternalApi->sns_message_controller_handle_message_0: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_one_base_code_controller_code**
> Code update_one_base_code_controller_code(body, id)

Update one Code

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.InternalApi(swagger_client.ApiClient(configuration))
body = swagger_client.Code() # Code | 
id = 'id_example' # str | 

try:
    # Update one Code
    api_response = api_instance.update_one_base_code_controller_code(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InternalApi->update_one_base_code_controller_code: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Code**](Code.md)|  | 
 **id** | **str**|  | 

### Return type

[**Code**](Code.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_one_base_feature_category_controller_feature_category**
> FeatureCategory update_one_base_feature_category_controller_feature_category(body, id)

Update one FeatureCategory

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.InternalApi(swagger_client.ApiClient(configuration))
body = swagger_client.FeatureCategory() # FeatureCategory | 
id = 'id_example' # str | 

try:
    # Update one FeatureCategory
    api_response = api_instance.update_one_base_feature_category_controller_feature_category(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InternalApi->update_one_base_feature_category_controller_feature_category: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FeatureCategory**](FeatureCategory.md)|  | 
 **id** | **str**|  | 

### Return type

[**FeatureCategory**](FeatureCategory.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_one_base_feature_controller_feature**
> Feature update_one_base_feature_controller_feature(body, id)

Update one Feature

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.InternalApi(swagger_client.ApiClient(configuration))
body = swagger_client.Feature() # Feature | 
id = 'id_example' # str | 

try:
    # Update one Feature
    api_response = api_instance.update_one_base_feature_controller_feature(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InternalApi->update_one_base_feature_controller_feature: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Feature**](Feature.md)|  | 
 **id** | **str**|  | 

### Return type

[**Feature**](Feature.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_one_base_feature_sub_category_controller_feature_sub_category**
> FeatureSubCategory update_one_base_feature_sub_category_controller_feature_sub_category(body, id)

Update one FeatureSubCategory

### Example
```python
from __future__ import print_function
import time
import curia.api.swagger_client
from curia.api.swagger_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = swagger_client.Configuration()
configuration.api_key['Api-Key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Api-Key'] = 'Bearer'

# create an instance of the API class
api_instance = swagger_client.InternalApi(swagger_client.ApiClient(configuration))
body = swagger_client.FeatureSubCategory() # FeatureSubCategory | 
id = 'id_example' # str | 

try:
    # Update one FeatureSubCategory
    api_response = api_instance.update_one_base_feature_sub_category_controller_feature_sub_category(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InternalApi->update_one_base_feature_sub_category_controller_feature_sub_category: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FeatureSubCategory**](FeatureSubCategory.md)|  | 
 **id** | **str**|  | 

### Return type

[**FeatureSubCategory**](FeatureSubCategory.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

