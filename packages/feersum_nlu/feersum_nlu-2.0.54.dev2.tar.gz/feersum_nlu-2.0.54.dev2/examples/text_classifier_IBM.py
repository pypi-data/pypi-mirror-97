""" Example: Shows how to create, train and use a text classifier. """

import urllib3
import csv

import feersum_nlu
from feersum_nlu.rest import ApiException
from examples import feersumnlu_host, feersum_nlu_auth_token

# Configure API key authorization: APIKeyHeader
configuration = feersum_nlu.Configuration()

# configuration.api_key['AUTH_TOKEN'] = feersum_nlu_auth_token
configuration.api_key['X-Auth-Token'] = feersum_nlu_auth_token  # Alternative auth key header!

configuration.host = feersumnlu_host

api_instance = feersum_nlu.TextClassifiersApi(feersum_nlu.ApiClient(configuration))

instance_name = 'intent_multi'

create_details = feersum_nlu.TextClassifierCreateDetails(name=instance_name,
                                                         desc="Intent classifier for Vodacom POC.",
                                                         load_from_store=False)

# The training samples.
labelled_train_sample_list = []

with open("text_classifier_IBM_train.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')

    for row in reader:
        label = row[0]
        text = row[1]
        lang_code = row[2]

        labelled_train_sample_list.append(feersum_nlu.LabelledTextSample(text=text,
                                                                         label=label,
                                                                         lang_code=lang_code))

# The testing samples.
labelled_test_sample_list = []

with open("text_classifier_IBM_test.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')

    for row in reader:
        label = row[0]
        text = row[1]
        lang_code = row[2]

        labelled_test_sample_list.append(feersum_nlu.LabelledTextSample(text=text,
                                                                        label=label,
                                                                        lang_code=lang_code))

train_details = feersum_nlu.TrainDetails(immediate_mode=True,
                                         threshold=0.9,
                                         temperature=0.5,
                                         clsfr_algorithm="fully_connected_neural_net",
                                         num_epochs=1000,
                                         language_model_list=[
                                             {
                                                 "lang_code": "xxx",
                                                 "lang_model": "feers_bpemb_zul"
                                             }
                                         ]
                                         )

text_input = feersum_nlu.TextInput("What is my balance?")

caller_name = 'example_caller'

print()

try:
    #    print("Update the model params:")
    #    model_params = feersum_nlu.ModelParams(readonly=False)
    #    api_response = api_instance.text_classifier_set_params(instance_name, model_params, x_caller=caller_name)
    #    print(" type(api_response)", type(api_response))
    #    print(" api_response", api_response)
    #    print()

    print("Create the text classifier:")
    api_response = api_instance.text_classifier_create(create_details)
    print(" type(api_response)", type(api_response))
    print(" api_response", api_response)
    print()

    print("Add training samples to the text classifier:")
    api_response = api_instance.text_classifier_add_training_samples(instance_name, labelled_train_sample_list)
    print(" type(api_response)", type(api_response))
    print(" api_response", api_response)
    print()

    print("Add testing samples to the text classifier:")
    api_response = api_instance.text_classifier_add_testing_samples(instance_name, labelled_test_sample_list)
    print(" type(api_response)", type(api_response))
    print(" api_response", api_response)
    print()

    print("Train the text classifier:")
    api_response = api_instance.text_classifier_train(instance_name, train_details)
    print(" type(api_response)", type(api_response))
    print(" api_response", api_response)
    print()

    print("Get the details of specific named loaded text classifiers:")
    api_response = api_instance.text_classifier_get_details(instance_name)
    print(" type(api_response)", type(api_response))
    print(" api_response", api_response)
    print()

    print("Get the labels of named loaded text classifiers:")
    api_response = api_instance.text_classifier_get_labels(instance_name)
    print(" type(api_response)", type(api_response))
    print(" api_response", api_response)
    print()

    print("Classify text:")
    api_response = api_instance.text_classifier_retrieve(instance_name, text_input, x_caller=caller_name)
    print(" type(api_response)", type(api_response))
    print(" api_response", api_response)
    print()

    # print("Update the model params:")
    # model_params = feersum_nlu.ModelParams(threshold=0.9, desc="Examples: Test text classifier.",
    #                                        long_name='Test Text Classifier',
    #                                        readonly=True)
    # api_response = api_instance.text_classifier_set_params(instance_name, model_params)
    # print(" type(api_response)", type(api_response))
    # print(" api_response", api_response)
    # print()

    print("Get the details of specific named loaded text classifiers:")
    api_response = api_instance.text_classifier_get_details(instance_name)
    print(" type(api_response)", type(api_response))
    print(" api_response", api_response)
    print()

    # print("Delete named loaded text classifier:")
    # api_response = api_instance.text_classifier_del(instance_name)
    # print(" type(api_response)", type(api_response))
    # print(" api_response", api_response)
    # print()
    #
    # print("Vaporise named loaded text classifier:")
    # api_response = api_instance.text_classifier_vaporise(instance_name)
    # print(" type(api_response)", type(api_response))
    # print(" api_response", api_response)
    # print()
except ApiException as e:
    print("Exception when calling a text classifier operation: %s\n" % e)
except urllib3.exceptions.HTTPError as e:
    print("Connection HTTPError! %s\n" % e)
