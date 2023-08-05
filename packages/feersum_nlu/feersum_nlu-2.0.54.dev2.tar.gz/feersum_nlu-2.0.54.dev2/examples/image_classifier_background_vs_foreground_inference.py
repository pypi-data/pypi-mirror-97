""" Example: Shows how to use an image classifier. """

import urllib3
import random

from typing import List, Tuple

import feersum_nlu
from feersum_nlu.rest import ApiException
from examples import feersumnlu_host, feersum_nlu_auth_token

from feersum_nlu_util import image_utils

# Configure API key authorization: APIKeyHeader
configuration = feersum_nlu.Configuration()

# configuration.api_key['AUTH_TOKEN'] = feersum_nlu_auth_token
configuration.api_key['X-Auth-Token'] = feersum_nlu_auth_token  # Alternative auth key header!

configuration.host = feersumnlu_host

api_instance = feersum_nlu.ImageClassifiersApi(feersum_nlu.ApiClient(configuration))

instance_name = 'DrOetker_fg_vs_bg_image_clsfr'
bg_all_data_path = "/Users/bduvenhage/Desktop/DrOetker_original/all"
labels = ["over", "under", "well"]

# === Load the data samples ===
print("Loading data samples...", end='', flush=True)
sample_list = []  # type: List[Tuple[str, str]]

for label in labels:
    bg_samples = image_utils.get_image_samples(bg_all_data_path, label,
                                               max_samples=1000,
                                               random_crop=512,
                                               repeat=9)

    # for i in range(20):
    #     image_utils.save_image(file_name="temp.png", base64_image_str=bg_samples[i][0])
    #     image_utils.show_image(file_name="temp.png")

    bg_num_samples = len(bg_samples)

    # 'bg' samples.
    sample_list.extend([(image, "bg") for image, _ in bg_samples])

print("done.")

num_samples = len(sample_list)
random.shuffle(sample_list)

samples = [feersum_nlu.LabelledImageSample(image=image, label=label) for image, label in sample_list]
# === ===

caller_name = 'example_caller'

print()

try:
    for i in range(num_samples):
        print("Classify image:")
        image_utils.save_image(file_name="temp.png", base64_image_str=samples[i].image)
        image_utils.show_image(file_name="temp.png")

        api_response = api_instance.image_classifier_retrieve(instance_name,
                                                              feersum_nlu.ImageInput(samples[i].image),
                                                              x_caller=caller_name)
        print(" type(api_response)", type(api_response))
        print(" api_response", api_response)
        print()

        input("Press Enter to continue...")

except ApiException as e:
    print("Exception when calling a image classifier operation: %s\n" % e)
except urllib3.exceptions.HTTPError as e:
    print("Connection HTTPError! %s\n" % e)
