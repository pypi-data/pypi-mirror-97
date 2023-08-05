""" Example: Shows how to use data objects and list the interactions. """

import urllib3
from typing import Dict

import feersum_nlu
from feersum_nlu.rest import ApiException
from examples import feersumnlu_host, feersum_nlu_auth_token

configuration = feersum_nlu.Configuration()
configuration.api_key['X-Auth-Token'] = feersum_nlu_auth_token  # Alternative auth key header!
configuration.host = feersumnlu_host

api_instance = feersum_nlu.DataObjectsApi(feersum_nlu.ApiClient(configuration))

print()

data_object_dict = {}  # type: Dict[str,Dict]

try:
    print("Get the names of all data objects:")
    object_name_list = api_instance.data_object_get_names_all()
    print(" type(api_response)", type(object_name_list))
    print(" api_response", object_name_list)
    print()

    print("GET-ing all the objects...", flush=True, end='')
    for object_name in object_name_list:
        try:
            # print("Get the details of specific named data object:")
            api_response = api_instance.data_object_get_details(object_name)
            # print(" type(api_response)", type(api_response))
            # print(" api_response", api_response)
            # print()
            data_object_dict[object_name] = api_response
            print(".", end='')
        except ApiException as e:
            print("Exception when calling a data object operation: %s\n" % e)
    print('done.')

    print("Listing the objects...", flush=True)
    for name, object in data_object_dict.items():
        print('.', end='')

        research_ID = object.get("researchID")
        if (research_ID is not None) and (research_ID.lower() != 'none'):
            print(research_ID)

            history = object.get('history')

            if history is not None:
                for obj in history:
                    tmstmp = obj.get('timestamp')
                    if tmstmp is not None:
                        print('   ', tmstmp)

            last_timestamp = object.get('timestamp')
            if last_timestamp is not None:
                print('   ', last_timestamp)

            print()

    print('done.')

except ApiException as e:
    print("Exception when calling a data object operation: %s\n" % e)
except urllib3.exceptions.HTTPError as e:
    print("Connection HTTPError! %s\n" % e)
