""" Example: Shows how to create & train an Intent classifier from a CSV file. """

import urllib3
import csv
import random

import feersum_nlu
from feersum_nlu.rest import ApiException
from examples import feersumnlu_host, feersum_nlu_auth_token

# Configure API key authorization: APIKeyHeader
configuration = feersum_nlu.Configuration()

# configuration.api_key['AUTH_TOKEN'] = feersum_nlu_auth_token
configuration.api_key['X-Auth-Token'] = feersum_nlu_auth_token  # Alternative auth key header!

configuration.host = feersumnlu_host

api_instance = feersum_nlu.IntentClassifiersApi(feersum_nlu.ApiClient(configuration))

instance_name = 'navigation_test'

create_details = feersum_nlu.IntentClassifierCreateDetails(name=instance_name,
                                                           lid_model_file="lid_za",
                                                           load_from_store=False)


def get_training_samples(month: str):
    training_sample_list = []

    with open(f'dstv_training_samples_{month}.csv',
              'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile,
                                delimiter=',',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)

        next(csvfile)  # Skip the first row with the labels.

        for row in csv_reader:
            training_sample_list.append(feersum_nlu.LabelledTextSample(text=row[1],
                                                                       label=row[0],
                                                                       lang_code=None))
    return training_sample_list


def get_utterances(base_name: str, month: str):
    dstv_utterance_file = f"{base_name}_{month}_2020 - utterances"

    with open(f'{dstv_utterance_file}.txt',
              'r') as txtfile:
        user_utterances = txtfile.readlines()

    random.shuffle(user_utterances)

    # return user_utterances[:(len(user_utterances)//10)]
    return user_utterances[:10000]


word_manifold_list = [feersum_nlu.LabelledWordManifold('eng', 'feers_wm_eng')]
# The playground's pre-loaded embeddings include:
# "feers_wm_afr", "feers_wm_eng", "feers_wm_nbl", "feers_wm_xho",
# "feers_wm_zul", "feers_wm_ssw", "feers_wm_nso", "feers_wm_sot",
# "feers_wm_tsn", "feers_wm_ven", "feers_wm_tso"
# and "glove6B50D_trimmed"

immediate_mode = True  # Set to True to do a blocking train operation.
train_details = feersum_nlu.TrainDetails(threshold=0.95,
                                         word_manifold_list=word_manifold_list,
                                         immediate_mode=immediate_mode)

caller_name = 'example_caller'

print()

try:
    base_names = [
        "Reconnect_Package_All_Utterances",
        "Change_Package_All_Utterances",
    ]
    months = ['June', 'July']

    for month in months:
        print("Create the Intent classifier:")
        api_response = api_instance.intent_classifier_create(create_details, x_caller=caller_name)
        print(" type(api_response)", type(api_response))
        print(" api_response", api_response)
        print()

        training_sample_list = get_training_samples(month)

        print("Add training samples to the Intent classifier:")
        api_response = api_instance.intent_classifier_add_training_samples(instance_name,
                                                                           training_sample_list)
        print(" type(api_response)", type(api_response))
        # print(" api_response", api_response)
        print()

        print("Train the Intent classifier:")
        instance_detail = api_instance.intent_classifier_train(instance_name, train_details)
        print(" type(api_response)", type(instance_detail))
        print(" api_response", instance_detail)
        print()

        for base_name in base_names:
            print()
            print(f"### base_name={base_name}, month={month} ###")

            user_utterances = get_utterances(base_name, month)
            unmatched_count = 0

            output_file = f"{base_name}_{month}_2020 - utterances"

            with open(f"{output_file}_pred_labels.csv", "w", newline='') as csvfile:
                csv_writer = csv.writer(csvfile,
                                        delimiter=',',
                                        quotechar='"',
                                        quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow(['label', 'text'])

                for index, text in enumerate(user_utterances):
                    text_input = feersum_nlu.TextInput(text.strip())
                    api_response = api_instance.intent_classifier_retrieve(instance_name, text_input, x_caller=caller_name)
                    # print("text_input", text_input)
                    # print(" type(api_response)", type(api_response))
                    # print(" api_response", api_response)
                    if len(api_response) == 0:
                        unmatched_count += 1
                        pred_label = '_nc'
                    else:
                        pred_label = api_response[0].label

                    csv_writer.writerow([pred_label, text.strip()])
                    if (index % (len(user_utterances) // 10)) == 0:
                        print(f'progress={round(10000.0 * index / len(user_utterances)) / 100.0}%, '
                              f'unmatched={round(10000.0 * unmatched_count / (index + 1)) / 100.0}%')

        print("Delete specific named loaded Intent classifier:")
        api_response = api_instance.intent_classifier_del(instance_name)
        print(" type(api_response)", type(api_response))
        print(" api_response", api_response)
        print()

        print("Vaporise specific named loaded Intent classifier:")
        api_response = api_instance.intent_classifier_vaporise(instance_name)
        print(" type(api_response)", type(api_response))
        print(" api_response", api_response)
        print()

except ApiException as e:
    print("Exception when calling an Intent classifier operation: %s\n" % e)
except urllib3.exceptions.HTTPError as e:
    print("Connection HTTPError! %s\n" % e)
