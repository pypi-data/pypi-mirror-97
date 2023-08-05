""" Example: Shows how to use data objects and list the interactions. """

import urllib3

import feersum_nlu
from feersum_nlu.rest import ApiException
from examples import feersumnlu_host, feersum_nlu_auth_token

configuration = feersum_nlu.Configuration()
configuration.api_key['X-Auth-Token'] = feersum_nlu_auth_token  # Alternative auth key header!
configuration.host = feersumnlu_host

api_instance = feersum_nlu.DataObjectsApi(feersum_nlu.ApiClient(configuration))

print()

try:
    print("Get the names of all data objects:")
    object_name_list = api_instance.data_object_get_names_all()
    print(" type(api_response)", type(object_name_list))
    print(" api_response", object_name_list)
    print()

    print("Fixing all the objects...", flush=True, end='')
    for object_name in object_name_list:
        try:
            # print("Get the details of specific named data object:")
            data = api_instance.data_object_get_details(object_name)
            # print(" type(api_response)", type(api_response))
            # print(" api_response", api_response)
            # print()
            print(".", end='')
            research_id = data.get("researchID")

            if (research_id is None) or (research_id == "None"):
                history = data.get("history")

                if history is not None:
                    for snapshot in history:
                        ss_rID = snapshot.get("researchID")
                        if (ss_rID is not None) and (ss_rID != "None"):
                            print(object_name, research_id, end=" ")
                            print("=>", ss_rID)

                            data["researchID"] = ss_rID
                            api_response = api_instance.data_object_post(object_name, data)
                            print(api_response, api_response)
                            break

            # api_response = api_instance.data_object_post(object_name, data)

        except ApiException as e:
            print("Exception when calling a data object operation: %s\n" % e)
    print('done.')

except ApiException as e:
    print("Exception when calling a data object operation: %s\n" % e)
except urllib3.exceptions.HTTPError as e:
    print("Connection HTTPError! %s\n" % e)
