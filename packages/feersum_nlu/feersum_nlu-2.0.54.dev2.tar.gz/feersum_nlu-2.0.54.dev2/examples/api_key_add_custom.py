""" Example: Shows how to create and manage API keys. """

import urllib3

import feersum_nlu
from feersum_nlu.rest import ApiException
from examples import feersumnlu_host, feersum_nlu_auth_token

# Configure API key authorization: APIKeyHeader
configuration = feersum_nlu.Configuration()

# configuration.api_key['AUTH_TOKEN'] = feersum_nlu_auth_token
configuration.api_key['X-Auth-Token'] = feersum_nlu_auth_token  # Alternative auth key header!

configuration.host = feersumnlu_host

api_instance = feersum_nlu.ApiKeysApi(feersum_nlu.ApiClient(configuration))

print()

try:
    print("Add an API key entry given the key:")

    new_custom_key = 'FEERSUM-NLU-431-9020-80dd-cec1569-QA'

    # Create a new random key.
    update_details = feersum_nlu.ApiKeyCreateDetails(desc="MassMart-QA")  # , call_count_limit=5000)

    # Update the key to new_custom_key value.
    api_response = api_instance.api_key_update_details(instance_name=new_custom_key, create_details=update_details)

    print(" type(api_response)", type(api_response))
    print(" api_response", api_response)
    print()

except ApiException as e:
    print("Exception when calling an api key operation: %s\n" % e)
except urllib3.exceptions.HTTPError as e:
    print("Connection HTTPError! %s\n" % e)
